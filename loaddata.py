#!/usr/bin/env python3
"""
Data Ingestion Script for E-commerce Chatbot
Parses CSV files and populates the database
"""

import os
import sys
import json
import csv
import pandas as pd
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random

# Database imports
try:
    import psycopg2
    from sqlalchemy import create_engine, text
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

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_ingestion.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DataValidator:
    """Data validation and cleaning utilities"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text data"""
        if pd.isna(text) or text is None:
            return ""
        return str(text).strip()
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Basic email validation"""
        if not email or '@' not in email:
            return False
        return True
    
    @staticmethod
    def validate_price(price: Any) -> Optional[float]:
        """Validate and convert price to float"""
        try:
            if pd.isna(price):
                return None
            price_float = float(str(price).replace('$', '').replace(',', ''))
            return price_float if price_float >= 0 else None
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def validate_integer(value: Any) -> Optional[int]:
        """Validate and convert to integer"""
        try:
            if pd.isna(value):
                return None
            return int(float(value))
        except (ValueError, TypeError):
            return None

class CSVDataIngestion:
    """Main data ingestion class"""
    
    def __init__(self, db_type: str, connection_config: Dict[str, Any]):
        self.db_type = db_type.lower()
        self.connection_config = connection_config
        self.connection = None
        self.engine = None
        self.validator = DataValidator()
        
        # Statistics
        self.stats = {
            'categories': {'processed': 0, 'inserted': 0, 'errors': 0},
            'products': {'processed': 0, 'inserted': 0, 'errors': 0},
            'orders': {'processed': 0, 'inserted': 0, 'errors': 0},
            'order_items': {'processed': 0, 'inserted': 0, 'errors': 0},
            'users': {'processed': 0, 'inserted': 0, 'errors': 0},
            'conversations': {'processed': 0, 'inserted': 0, 'errors': 0}
        }
    
    def connect(self) -> bool:
        """Connect to the database"""
        try:
            if self.db_type == "postgresql":
                self.connection = psycopg2.connect(**self.connection_config)
                db_url = f"postgresql://{self.connection_config['user']}:{self.connection_config['password']}@{self.connection_config['host']}:{self.connection_config['port']}/{self.connection_config['database']}"
                self.engine = create_engine(db_url)
                
            elif self.db_type == "mysql":
                self.connection = mysql.connector.connect(**self.connection_config)
                db_url = f"mysql+mysqlconnector://{self.connection_config['user']}:{self.connection_config['password']}@{self.connection_config['host']}:{self.connection_config['port']}/{self.connection_config['database']}"
                self.engine = create_engine(db_url)
                
            elif self.db_type == "mongodb":
                if self.connection_config.get('username'):
                    connection_string = f"mongodb://{self.connection_config['username']}:{self.connection_config['password']}@{self.connection_config['host']}:{self.connection_config['port']}/{self.connection_config['database']}"
                else:
                    connection_string = f"mongodb://{self.connection_config['host']}:{self.connection_config['port']}"
                
                self.connection = MongoClient(connection_string)
                self.db = self.connection[self.connection_config['database']]
            
            logger.info(f"Connected to {self.db_type} database")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False
    
    def load_categories_csv(self, csv_file: str) -> bool:
        """Load categories from CSV file"""
        logger.info(f"Loading categories from {csv_file}")
        
        try:
            # Read CSV
            df = pd.read_csv(csv_file)
            logger.info(f"Read {len(df)} rows from categories CSV")
            
            # Validate required columns
            required_columns = ['name']
            if not all(col in df.columns for col in required_columns):
                logger.error(f"Missing required columns. Expected: {required_columns}")
                return False
            
            # Clean and validate data
            df['name'] = df['name'].apply(self.validator.clean_text)
            df['description'] = df.get('description', '').apply(self.validator.clean_text)
            
            # Remove empty names
            df = df[df['name'] != '']
            
            # Remove duplicates
            df = df.drop_duplicates(subset=['name'])
            
            self.stats['categories']['processed'] = len(df)
            
            if self.db_type in ['postgresql', 'mysql']:
                # SQL database insertion
                df.to_sql('categories', self.engine, if_exists='append', index=False, method='multi')
                self.stats['categories']['inserted'] = len(df)
                
            elif self.db_type == 'mongodb':
                # MongoDB insertion
                records = df.to_dict('records')
                for record in records:
                    record['created_at'] = datetime.now()
                
                if records:
                    self.db.categories.insert_many(records)
                    self.stats['categories']['inserted'] = len(records)
            
            logger.info(f"Successfully inserted {len(df)} categories")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load categories: {e}")
            self.stats['categories']['errors'] += 1
            return False
    
    def load_products_csv(self, csv_file:
