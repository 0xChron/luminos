import duckdb
import pandas as pd
from ingest.config import Config

class DuckDBLoader:
    def __init__(self, db_path: str = Config.DUCKDB_PATH):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.conn = duckdb.connect(self.db_path)
        self._init_tables()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            
    def _init_tables(self):
        # solar energy fact table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS fact_solar_energy_data (
                timestamp TIMESTAMP PRIMARY KEY,
                generation DOUBLE,
                consumption DOUBLE,
                grid_feed_in DOUBLE,
                grid_purchased DOUBLE,
                charge_value DOUBLE,
                discharge_value DOUBLE,
                loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # weather hourly dimension
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS dim_weather_data_hourly (
                timestamp TIMESTAMP PRIMARY KEY,
                temperature_2m DOUBLE,
                cloud_cover DOUBLE,
                precipitation DOUBLE,
                wind_speed_10m DOUBLE,
                relative_humidity_2m DOUBLE,
                weather_code INTEGER,
                loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # weather daily dimension
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS dim_weather_data_daily (
                date DATE PRIMARY KEY,
                shortwave_radiation_sum DOUBLE,
                sunshine_duration DOUBLE,
                daylight_duration DOUBLE,
                uv_index_clear_sky_max DOUBLE,
                temperature_2m_max DOUBLE,
                temperature_2m_min DOUBLE,
                loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def load_solar_data(self, df: pd.DataFrame) -> int:
        if df.empty:
            return 0
        
        # delete existing records for the date range
        min_date = df['timestamp'].min().date()
        max_date = df['timestamp'].max().date()
        
        self.conn.execute(f"""
            DELETE FROM fact_solar_energy_data 
            WHERE DATE(timestamp) BETWEEN '{min_date}' AND '{max_date}'
        """)
        
        # insert new records
        self.conn.execute("""
            INSERT INTO fact_solar_energy_data 
            (
                timestamp, 
                generation,
                consumption,
                grid_feed_in, 
                grid_purchased,
                charge_value,
                discharge_value
            )
            SELECT 
                timestamp, 
                generation,
                consumption,
                grid_feed_in,
                grid_purchased, 
                charge_value,
                discharge_value
            FROM df
        """)
        
        return len(df)
    
    def load_weather_hourly(self, df: pd.DataFrame) -> int:
        if df.empty:
            return 0
        
        self.conn.execute("""
            INSERT OR REPLACE INTO dim_weather_data_hourly 
            (
                timestamp, 
                temperature_2m,
                cloud_cover,
                precipitation,
                wind_speed_10m, 
                relative_humidity_2m, 
                weather_code
            )
            SELECT * FROM df
        """)
        
        return len(df)
    
    def load_weather_daily(self, df: pd.DataFrame) -> int:
        if df.empty:
            return 0
        
        self.conn.execute("""
            INSERT OR REPLACE INTO dim_weather_data_daily 
            (
                date, 
                shortwave_radiation_sum, 
                sunshine_duration,
                daylight_duration, 
                uv_index_clear_sky_max,
                temperature_2m_max, 
                temperature_2m_min
            )
            SELECT * FROM df
        """)
        
        return len(df)