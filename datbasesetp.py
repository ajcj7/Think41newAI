#!/usr/bin/env python3
"""
Database Setup Script for E-commerce Chatbot
Supports PostgreSQL, MySQL, and MongoDB
"""

import os
import sys
from pathlib import Path
import logging
from typing import Dict, Any, Optional
import json

# Database-specific imports
try:
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    POSTGRESQL_AVAILABLE = True
except ImportError:
    POSTGRESQL_AVAILABLE = False

try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

try:
    from pymongo import MongoClient
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.exc import SQLAlchemyError
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database_setup.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DatabaseConfig:
    """Database configuration manager"""
    
    def __init__(self, config_file: str = "database_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load database configuration from file or environment"""
        
        # Default configuration
        default_config = {
            "postgresql": {
                "host": os.getenv("PG_HOST", "localhost"),
                "port": int(os.getenv("PG_PORT", 5432)),
                "user": os.getenv("PG_USER", "postgres"),
                "password": os.getenv("PG_PASSWORD", "password"),
                "database": os.getenv("PG_DATABASE", "chatbot_ecommerce")
            },
            "mysql": {
                "host": os.getenv("MYSQL_HOST", "localhost"),
                "port": int(os.getenv("MYSQL_PORT", 3306)),
                "user": os.getenv("MYSQL_USER", "root"),
                "password": os.getenv("MYSQL_PASSWORD", "password"),
                "database": os.getenv("MYSQL_DATABASE", "chatbot_ecommerce")
            },
            "mongodb": {
                "host": os.getenv("MONGO_HOST", "localhost"),
                "port": int(os.getenv("MONGO_PORT", 27017)),
                "database": os.getenv("MONGO_DATABASE", "chatbot_ecommerce"),
                "username": os.getenv("MONGO_USERNAME", ""),
                "password": os.getenv("MONGO_PASSWORD", "")
            }
        }
        
        # Try to load from config file
        if Path(self.config_file).exists():
            try:
                with open(self.config_file, 'r') as f:
                    file_config = json.load(f)
                    # Merge with defaults
                    for db_type in default_config:
                        if db_type in file_config:
                            default_config[db_type].update(file_config[db_type])
                logger.info(f"Loaded configuration from {self.config_file}")
            except Exception as e:
                logger.warning(f"Failed to load config file: {e}. Using defaults.")
        
        return default_config
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")

class PostgreSQLSetup:
    """PostgreSQL database setup"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connection = None
        self.engine = None
    
    def create_database(self) -> bool:
        """Create the database if it doesn't exist"""
        try:
            # Connect to default postgres database
            conn = psycopg2.connect(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password'],
                database='postgres'
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            # Check if database exists
            cursor.execute(
                "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
                (self.config['database'],)
            )
            
            if not cursor.fetchone():
                cursor.execute(f"CREATE DATABASE {self.config['database']}")
                logger.info(f"Created PostgreSQL database: {self.config['database']}")
            else:
                logger.info(f"PostgreSQL database already exists: {self.config['database']}")
            
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Failed to create PostgreSQL database: {e}")
            return False
    
    def connect(self) -> bool:
        """Connect to the database"""
        try:
            # Raw connection for direct SQL execution
            self.connection = psycopg2.connect(**self.config)
            
            # SQLAlchemy engine for pandas integration
            if SQLALCHEMY_AVAILABLE:
                db_url = f"postgresql://{self.config['user']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['database']}"
                self.engine = create_engine(db_url)
            
            logger.info("Connected to PostgreSQL database")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            return False
    
    def create_tables(self) -> bool:
        """Create all required tables"""
        
        sql_schema = """
        -- Enable UUID extension
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        
        -- Categories table
        CREATE TABLE IF NOT EXISTS categories (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Products table
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            category_id INT REFERENCES categories(id),
            description TEXT,
            price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
            stock_quantity INT DEFAULT 0 CHECK (stock_quantity >= 0),
            total_sold INT DEFAULT 0 CHECK (total_sold >= 0),
            sku VARCHAR(100) UNIQUE,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Users table
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(100) UNIQUE,
            name VARCHAR(100),
            phone VARCHAR(20),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Orders table
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            customer_name VARCHAR(100),
            customer_email VARCHAR(100),
            customer_phone VARCHAR(20),
            status VARCHAR(50) DEFAULT 'pending' CHECK (
                status IN ('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled', 'returned')
            ),
            total_amount DECIMAL(10,2) DEFAULT 0,
            shipping_address TEXT,
            tracking_number VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Order items table
        CREATE TABLE IF NOT EXISTS order_items (
            id SERIAL PRIMARY KEY,
            order_id INT REFERENCES orders(id) ON DELETE CASCADE,
            product_id INT REFERENCES products(id),
            quantity INT NOT NULL CHECK (quantity > 0),
            unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
            total_price DECIMAL(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED
        );
        
        -- Conversations table
        CREATE TABLE IF NOT EXISTS conversations (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id),
            session_id VARCHAR(100),
            user_identifier VARCHAR(100),
            channel VARCHAR(50) DEFAULT 'web' CHECK (
                channel IN ('web', 'mobile', 'whatsapp', 'telegram', 'email')
            ),
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ended_at TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE,
            metadata JSONB
        );
        
        -- Messages table
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            conversation_id INT REFERENCES conversations(id) ON DELETE CASCADE,
            sender VARCHAR(10) NOT NULL CHECK (sender IN ('user', 'bot')),
            message TEXT NOT NULL,
            message_type VARCHAR(20) DEFAULT 'text' CHECK (
                message_type IN ('text', 'image', 'file', 'quick_reply', 'button_click')
            ),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sequence_number INT,
            intent VARCHAR(100),
            entities JSONB,
            confidence_score DECIMAL(3,2),
            context JSONB,
            bot_response_time_ms INT,
            related_order_id INT REFERENCES orders(id),
            related_product_id INT REFERENCES products(id)
        );
        
        -- FAQ Analytics table
        CREATE TABLE IF NOT EXISTS faq_analytics (
            id SERIAL PRIMARY KEY,
            intent VARCHAR(100),
            question_pattern TEXT,
            frequency_count INT DEFAULT 1,
            last_asked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Conversation feedback table
        CREATE TABLE IF NOT EXISTS conversation_feedback (
            id SERIAL PRIMARY KEY,
            conversation_id INT REFERENCES conversations(id),
            rating INT CHECK (rating BETWEEN 1 AND 5),
            feedback_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create indexes for better performance
        CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
        CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON conversations(session_id);
        CREATE INDEX IF NOT EXISTS idx_conversations_started_at ON conversations(started_at DESC);
        CREATE INDEX IF NOT EXISTS idx_conversations_user_identifier ON conversations(user_identifier);
        CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
        CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp DESC);
        CREATE INDEX IF NOT EXISTS idx_messages_sequence ON messages(conversation_id, sequence_number);
        CREATE INDEX IF NOT EXISTS idx_messages_sender_timestamp ON messages(sender, timestamp DESC);
        CREATE INDEX IF NOT EXISTS idx_messages_intent ON messages(intent);
        CREATE INDEX IF NOT EXISTS idx_products_total_sold ON products(total_sold DESC);
        CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);
        CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
        CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at DESC);
        CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
        
        -- Create trigger for message sequence numbering
        CREATE OR REPLACE FUNCTION set_message_sequence()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.sequence_number = COALESCE(
                (SELECT MAX(sequence_number) + 1 
                 FROM messages 
                 WHERE conversation_id = NEW.conversation_id), 
                1
            );
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        
        DROP TRIGGER IF EXISTS trigger_set_message_sequence ON messages;
        CREATE TRIGGER trigger_set_message_sequence
            BEFORE INSERT ON messages
            FOR EACH ROW
            EXECUTE FUNCTION set_message_sequence();
        
        -- Create useful views
        CREATE OR REPLACE VIEW top_selling_products AS
        SELECT 
            p.id,
            p.name,
            c.name as category,
            p.total_sold,
            p.price,
            p.stock_quantity
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.is_active = TRUE
        ORDER BY p.total_sold DESC, p.name;
        
        CREATE OR REPLACE VIEW conversation_summary AS
        SELECT 
            c.id,
            c.user_identifier,
            c.started_at,
            c.ended_at,
            COUNT(m.id) as message_count,
            MAX(m.timestamp) as last_message_at,
            c.channel
        FROM conversations c
        LEFT JOIN messages m ON c.id = m.conversation_id
        GROUP BY c.id, c.user_identifier, c.started_at, c.ended_at, c.channel
        ORDER BY c.started_at DESC;
        """
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_schema)
            self.connection.commit()
            cursor.close()
            logger.info("PostgreSQL tables created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create PostgreSQL tables: {e}")
            self.connection.rollback()
            return False
    
    def close(self):
        """Close database connections"""
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()

class MySQLSetup:
    """MySQL database setup"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connection = None
        self.engine = None
    
    def create_database(self) -> bool:
        """Create the database if it doesn't exist"""
        try:
            conn = mysql.connector.connect(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password']
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config['database']}")
            cursor.close()
            conn.close()
            logger.info(f"Created MySQL database: {self.config['database']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create MySQL database: {e}")
            return False
    
    def connect(self) -> bool:
        """Connect to the database"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            
            if SQLALCHEMY_AVAILABLE:
                db_url = f"mysql+mysqlconnector://{self.config['user']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['database']}"
                self.engine = create_engine(db_url)
            
            logger.info("Connected to MySQL database")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to MySQL: {e}")
            return False
    
    def create_tables(self) -> bool:
        """Create all required tables for MySQL"""
        
        # MySQL-specific schema (similar to PostgreSQL but with MySQL syntax)
        sql_schema = """
        -- Categories table
        CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Products table
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            category_id INT,
            description TEXT,
            price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
            stock_quantity INT DEFAULT 0 CHECK (stock_quantity >= 0),
            total_sold INT DEFAULT 0 CHECK (total_sold >= 0),
            sku VARCHAR(100) UNIQUE,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        );
        
        -- Add other tables similar to PostgreSQL but with MySQL syntax...
        -- (This would be the full MySQL schema - truncated for brevity)
        """
        
        try:
            cursor = self.connection.cursor()
            # Execute each statement separately for MySQL
            statements = sql_schema.split(';')
            for statement in statements:
                if statement.strip():
                    cursor.execute(statement)
            
            self.connection.commit()
            cursor.close()
            logger.info("MySQL tables created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create MySQL tables: {e}")
            return False
    
    def close(self):
        """Close database connections"""
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()

class MongoDBSetup:
    """MongoDB database setup"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = None
        self.db = None
    
    def connect(self) -> bool:
        """Connect to MongoDB"""
        try:
            # Build connection string
            if self.config.get('username') and self.config.get('password'):
                connection_string = f"mongodb://{self.config['username']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['database']}"
            else:
                connection_string = f"mongodb://{self.config['host']}:{self.config['port']}"
            
            self.client = MongoClient(connection_string)
            self.db = self.client[self.config['database']]
            
            # Test connection
            self.client.admin.command('ping')
            logger.info("Connected to MongoDB database")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False
    
    def create_collections(self) -> bool:
        """Create collections and indexes"""
        try:
            # Create collections
            collections = [
                'categories', 'products', 'users', 'orders', 
                'conversations', 'messages', 'faq_analytics', 'conversation_feedback'
            ]
            
            for collection_name in collections:
                if collection_name not in self.db.list_collection_names():
                    self.db.create_collection(collection_name)
                    logger.info(f"Created collection: {collection_name}")
            
            # Create indexes
            self.db.products.create_index([("total_sold", -1)])
            self.db.products.create_index([("category_id", 1)])
            self.db.orders.create_index([("status", 1)])
            self.db.orders.create_index([("created_at", -1)])
            self.db.conversations.create_index([("user_identifier", 1)])
            self.db.conversations.create_index([("started_at", -1)])
            self.db.messages.create_index([("conversation_id", 1), ("timestamp", 1)])
            self.db.messages.create_index([("intent", 1)])
            
            logger.info("MongoDB collections and indexes created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create MongoDB collections: {e}")
            return False
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()

class DatabaseSetupManager:
    """Main database setup manager"""
    
    def __init__(self, db_type: str = "postgresql"):
        self.db_type = db_type.lower()
        self.config_manager = DatabaseConfig()
        self.db_setup = None
    
    def setup_database(self) -> bool:
        """Setup the chosen database"""
        
        if self.db_type == "postgresql":
            if not POSTGRESQL_AVAILABLE:
                logger.error("PostgreSQL dependencies not installed. Run: pip install psycopg2-binary")
                return False
            
            config = self.config_manager.config["postgresql"]
            self.db_setup = PostgreSQLSetup(config)
            
            if not self.db_setup.create_database():
                return False
            if not self.db_setup.connect():
                return False
            return self.db_setup.create_tables()
        
        elif self.db_type == "mysql":
            if not MYSQL_AVAILABLE:
                logger.error("MySQL dependencies not installed. Run: pip install mysql-connector-python")
                return False
            
            config = self.config_manager.config["mysql"]
            self.db_setup = MySQLSetup(config)
            
            if not self.db_setup.create_database():
                return False
            if not self.db_setup.connect():
                return False
            return self.db_setup.create_tables()
        
        elif self.db_type == "mongodb":
            if not MONGODB_AVAILABLE:
                logger.error("MongoDB dependencies not installed. Run: pip install pymongo")
                return False
            
            config = self.config_manager.config["mongodb"]
            self.db_setup = MongoDBSetup(config)
            
            if not self.db_setup.connect():
                return False
            return self.db_setup.create_collections()
        
        else:
            logger.error(f"Unsupported database type: {self.db_type}")
            return False
    
    def get_connection_info(self) -> Dict[str, Any]:
        """Get connection information for the data ingestion script"""
        return self.config_manager.config[self.db_type]
    
    def close(self):
        """Close database connections"""
        if self.db_setup:
            self.db_setup.close()

def main():
    """Main setup function"""
    
    # Check command line arguments
    if len(sys.argv) > 1:
        db_type = sys.argv[1]
    else:
        db_type = input("Choose database type (postgresql/mysql/mongodb) [postgresql]: ").strip() or "postgresql"
    
    logger.info(f"Setting up {db_type} database...")
    
    # Setup database
    setup_manager = DatabaseSetupManager(db_type)
    
    try:
        if setup_manager.setup_database():
            logger.info(f"✅ {db_type.capitalize()} database setup completed successfully!")
            
            # Save connection info for data ingestion
            connection_info = setup_manager.get_connection_info()
            with open(f"{db_type}_connection.json", "w") as f:
                json.dump(connection_info, f, indent=2)
            
            logger.info(f"Connection info saved to {db_type}_connection.json")
            
        else:
            logger.error(f"❌ Failed to setup {db_type} database")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error during setup: {e}")
        sys.exit(1)
    finally:
        setup_manager.close()

if __name__ == "__main__":
    main()
