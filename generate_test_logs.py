import pandas as pd
import numpy as np
import os

print("="*60)
print("Generating Test Network Logs")
print("="*60)

os.makedirs('network_logs', exist_ok=True)

np.random.seed(123)

test_data = {
    'packet_size': np.random.randint(50, 1500, 100),
    'duration': np.random.uniform(0.1, 300, 100),
    'src_bytes': np.random.randint(0, 30000, 100),
    'dst_bytes': np.random.randint(0, 30000, 100),
    'wrong_fragment': np.random.randint(0, 3, 100),
    'urgent': np.random.randint(0, 3, 100),
    'num_failed_logins': np.random.randint(0, 5, 100),
    'num_file_creations': np.random.randint(0, 10, 100),
    'num_access_files': np.random.randint(0, 15, 100),
    'count': np.random.randint(0, 500, 100),
    'srv_count': np.random.randint(0, 500, 100)
}

test_df = pd.DataFrame(test_data)

test_df.loc[10:15, 'wrong_fragment'] = 4
test_df.loc[10:15, 'num_failed_logins'] = 4
test_df.loc[20:25, 'packet_size'] = 1450
test_df.loc[20:25, 'duration'] = 250

output_file = 'network_logs/test_logs_001.csv'
test_df.to_csv(output_file, index=False)

print(f"\n Created: {output_file}")
print(f"Records: {len(test_df)}")
print("="*60)
