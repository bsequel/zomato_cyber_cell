import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from Z4_1_config import DB_CONFIG  # Your DB config

def export_cyber_fraud_data_to_excel():
    try:
        # Build connection string
        db_url = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"

        # Create SQLAlchemy engine
        engine = create_engine(db_url)

        # SQL Query
        query = "SELECT * FROM cyber_fraud_reports ORDER BY sno DESC"

        # Read data
        df = pd.read_sql(query, engine)

        # Create output folder if not exists
        output_folder = "excel_reports"
        os.makedirs(output_folder, exist_ok=True)

        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cyber_fraud_report_{timestamp}.xlsx"
        filepath = os.path.join(output_folder, filename)

        # Export to Excel
        df.to_excel(filepath, index=False, engine='openpyxl')
        print(f"✅ Excel report saved to: {filepath}")
        return filepath

    except Exception as e:
        print(f"❌ Failed to export report: {e}")
        return None

# Run
# if __name__ == "__main__":
#     export_cyber_fraud_data_to_excel()


































































# import os
# import pandas as pd
# import psycopg2
# from datetime import datetime
# from Z4_1_db_config import DB_CONFIG  # Adjust path if needed

# def export_cyber_fraud_data_to_excel():
#     try:
#         # Connect to PostgreSQL
#         conn = psycopg2.connect(**DB_CONFIG)

#         # SQL Query
#         query = "SELECT * FROM cyber_fraud_reports ORDER BY sno DESC;"

#         # Load data into a DataFrame
#         df = pd.read_sql(query, conn)

#         # Create output folder if not exists
#         output_folder = "excel_reports"
#         os.makedirs(output_folder, exist_ok=True)

#         # Create timestamped filename
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         filename = f"cyber_fraud_report_{timestamp}.xlsx"
#         filepath = os.path.join(output_folder, filename)

#         # Save DataFrame to Excel
#         df.to_excel(filepath, index=False, engine='openpyxl')
#         print(f"✅ Excel report saved to: {filepath}")

#         # Cleanup
#         conn.close()
#         return filepath

#     except Exception as e:
#         print(f"❌ Failed to export report: {e}")
#         return None

# # # Example usage
# # if __name__ == "__main__":
# #     export_cyber_fraud_data_to_excel()
