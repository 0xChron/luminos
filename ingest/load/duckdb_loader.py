import duckdb
import pandas as pd
from ingest.config import Config

class DuckDBLoader:
    def __init__(self, db_path: str = Config.DUCKDB_PATH):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.conn = duckdb.connect(self.db_path)
        self.conn.execute("CREATE SCHEMA IF NOT EXISTS raw;")
        self.conn.execute("SET schema 'raw';") 
        self._init_tables()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            
    def _init_tables(self):
        # solar energy 5 minute
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS raw_solar_energy_5_min (
                timestamp DOUBLE PRIMARY KEY,
                generation DOUBLE,
                consumption DOUBLE,
                grid_feed_in DOUBLE,
                grid_purchase DOUBLE,
                charge_power DOUBLE,
                discharge_power DOUBLE,
                battery_soc DOUBLE,
                loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # weather hourly
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS raw_weather_data_hourly (
                timestamp TIMESTAMPTZ PRIMARY KEY,
                relative_humidity_2m DOUBLE,
                wind_speed_10m DOUBLE,
                is_day INT,
                sunshine_duration DOUBLE,
                temperature_2m DOUBLE,
                cloud_cover DOUBLE,
                rain DOUBLE,
                weather_code INT,
                loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # weather daily 
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS raw_weather_data_daily (
                timestamp TIMESTAMPTZ PRIMARY KEY,
                shortwave_radiation_sum DOUBLE,
                sunshine_duration DOUBLE,
                daylight_duration DOUBLE,
                cloud_cover_mean DOUBLE,
                temperature_2m_mean DOUBLE,
                relative_humidity_2m_mean DOUBLE,
                rain_sum DOUBLE,
                wind_speed_10m_mean DOUBLE,
                weather_code INT,
                loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def load_solar_data(self, df: pd.DataFrame) -> int:
        if df.empty:
            return 0
        
        self.conn.execute("""
            INSERT OR REPLACE INTO raw_solar_energy_5_min 
            (
                timestamp, 
                generation,
                consumption,
                grid_feed_in, 
                grid_purchase,
                charge_power,
                discharge_power,
                battery_soc
            )
            SELECT 
                timestamp, 
                generation,
                consumption,
                grid_feed_in,
                grid_purchase, 
                charge_power,
                discharge_power,
                battery_soc
            FROM df
        """)
        
        return len(df)
    
    def load_weather_hourly(self, df: pd.DataFrame) -> int:
        if df.empty:
            return 0
        
        self.conn.execute("""
            INSERT OR REPLACE INTO raw_weather_data_hourly 
            (
                timestamp,
                relative_humidity_2m,
                wind_speed_10m,
                is_day,
                sunshine_duration,
                temperature_2m,
                cloud_cover,
                rain,
                weather_code
            )
            SELECT
                timestamp,
                relative_humidity_2m,
                wind_speed_10m,
                is_day,
                sunshine_duration,
                temperature_2m,
                cloud_cover,
                rain,
                weather_code
            FROM df
        """)
        
        return len(df)
    
    def load_weather_daily(self, df: pd.DataFrame) -> int:
        if df.empty:
            return 0
        
        self.conn.execute("""
            INSERT OR REPLACE INTO raw_weather_data_daily 
            (
                timestamp,
                shortwave_radiation_sum,
                sunshine_duration,
                daylight_duration,
                cloud_cover_mean,
                temperature_2m_mean,
                relative_humidity_2m_mean,
                rain_sum,
                wind_speed_10m_mean,
                weather_code
            )
            SELECT 
                timestamp,
                shortwave_radiation_sum,
                sunshine_duration,
                daylight_duration,
                cloud_cover_mean,
                temperature_2m_mean,
                relative_humidity_2m_mean,
                rain_sum,
                wind_speed_10m_mean,
                weather_code
            FROM df
        """)
            
        return len(df)