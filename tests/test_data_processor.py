import unittest
import pandas as pd
from datetime import datetime, timedelta
from data.data_processor import (
    convert_to_weekly, 
    convert_to_monthly, 
    calculate_growth_rate,
    calculate_moving_average,
    filter_by_date_range
)

class TestDataProcessor(unittest.TestCase):
    
    def setUp(self):
        # Create sample data for testing
        dates = [datetime.now() - timedelta(days=i) for i in range(30)]
        dates.reverse()  # Oldest to newest
        
        values = [100 + i * 10 for i in range(30)]  # Simple linear growth
        
        self.test_df = pd.DataFrame({
            'date': dates,
            'value': values
        })
    
    def test_convert_to_weekly(self):
        weekly_df = convert_to_weekly(self.test_df, 'date', 'value')
        
        # Check that we have the right number of weeks
        self.assertTrue(len(weekly_df) < len(self.test_df))
        
        # Check that the total sum is preserved
        self.assertAlmostEqual(
            weekly_df['value'].sum(), 
            self.test_df['value'].sum(),
            delta=1  # Allow for small rounding differences
        )
    
    def test_convert_to_monthly(self):
        monthly_df = convert_to_monthly(self.test_df, 'date', 'value')
        
        # Check that we have fewer rows than the original
        self.assertTrue(len(monthly_df) < len(self.test_df))
        
        # Check that each month has the expected columns
        self.assertTrue('month' in monthly_df.columns)
        self.assertTrue('year' in monthly_df.columns)
    
    def test_calculate_growth_rate(self):
        growth_df = calculate_growth_rate(self.test_df, 'value')
        
        # Check that the growth rate column exists
        self.assertTrue('growth_rate' in growth_df.columns)
        
        # The first row should have NaN for growth rate
        self.assertTrue(pd.isna(growth_df.iloc[0]['growth_rate']))
        
        # With our linear growth data, growth rate should decrease over time
        # as the same absolute change represents a smaller percentage
        for i in range(2, len(growth_df)-1):
            self.assertTrue(growth_df.iloc[i]['growth_rate'] <= growth_df.iloc[i-1]['growth_rate'])
    
    def test_calculate_moving_average(self):
        window = 7
        ma_df = calculate_moving_average(self.test_df, 'value', window=window)
        
        # Check that the MA column exists
        self.assertTrue(f'value_ma{window}' in ma_df.columns)
        
        # First (window-1) rows should have NaN for MA
        for i in range(window-1):
            self.assertTrue(pd.isna(ma_df.iloc[i][f'value_ma{window}']))
        
        # Check a specific calculation
        # For linear data, MA should equal the middle value
        middle_idx = window // 2
        for i in range(window-1, len(ma_df)):
            expected_ma = self.test_df.iloc[i-middle_idx]['value']
            actual_ma = ma_df.iloc[i][f'value_ma{window}']
            self.assertAlmostEqual(actual_ma, expected_ma, delta=window*5)  # Allow for some variation
    
    def test_filter_by_date_range(self):
        # Test filtering for last 7 days
        end_date = self.test_df['date'].max()
        start_date = end_date - timedelta(days=6)  # 7 days including end_date
        
        filtered_df = filter_by_date_range(self.test_df, 'date', start_date, end_date)
        
        # Should have 7 days of data
        self.assertEqual(len(filtered_df), 7)
        
        # Check date range
        self.assertEqual(filtered_df['date'].min(), start_date)
        self.assertEqual(filtered_df['date'].max(), end_date)

if __name__ == '__main__':
    unittest.main()