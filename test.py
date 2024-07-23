import unittest
import pandas as pd
import numpy as np
from wf_func import *

class TestCompareDataFrames(unittest.TestCase):

    def test_compare_dataframes(self):
        # Create original DataFrame
        original_data = {
            'A': [1, 2, 3],
            'B': [4, 5, 6],
            'C': [7, 8, 9]
        }
        original_df = pd.DataFrame(original_data)

        # Create updated DataFrame with some changes
        updated_data = {
            'A': [1, 2, 3],
            'B': [4, 10, 6],  # Change in second row
            'C': [7, 8, 10]   # Change in third row
        }
        updated_df = pd.DataFrame(updated_data)

        # Expected difference DataFrame
        expected_diff_data = {
            'A': [np.nan, np.nan, np.nan],
            'B': [np.nan, 10, np.nan],
            'C': [np.nan, np.nan, 10]
        }
        expected_diff_df = pd.DataFrame(expected_diff_data)
        # Compare dataframes
        diff_df = compare_dataframes(original_df, updated_df)
        pd.testing.assert_frame_equal(diff_df, expected_diff_df)
        visualize_diff(original_df, updated_df)

    def test_summarize_diff(self):
        # Create a difference DataFrame
        diff_data = {
            'A': [np.nan, np.nan, np.nan],
            'B': [np.nan, 10, np.nan],
            'C': [np.nan, np.nan, 10]
        }
        diff_df = pd.DataFrame(diff_data)
        # Expected summary DataFrame
        expected_summary_data = {
            'number_changes': [0, 1, 1,  2],
            'perc_changes': [0.0, 0.3333, 0.3333, 0.6667]
        }
        expected_summary_df = pd.DataFrame(expected_summary_data, index=['A', 'B', 'C', 'all_records'])

        # Summarize differences
        summary_df = summarize_diff(diff_df)

        # Assert the summary DataFrame is as expected
        pd.testing.assert_frame_equal(summary_df, expected_summary_df)


if __name__ == '__main__':
    unittest.main()