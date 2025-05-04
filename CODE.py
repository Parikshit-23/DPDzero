# Importing all the necessary required libraries
import pandas as pd
import argparse
import logging
from datetime import datetime


# SETUP #

def setup_logging():
    # This function will help to generate all the logging
    # All the logging will be stored in a text file 'agent_analysis.log'
    
    # Here the format of logging is defined in the placeholder '%(asctime)s - %(levelname)s - %(message)s'
    # %(asctime)s = timestamp of when the log entry was created (eg : 2025/05/04 13:24:00)
    # %(levelname)s = log level (eg : INFO,ERROR)
    # %(message)S = log message text you passed to logging.info()
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("agent_analysis.log"),
            logging.StreamHandler()
        ]
    )

def parse_args():
    # This function will help to communicate in command-line environment
    # It will handle the commands in CMD
    parser = argparse.ArgumentParser(description="Agent Performance Analyzer")
    parser.add_argument('--roster', required=True, help='Path to agent_roster.csv')
    parser.add_argument('--logs', required=True, help='Path to call_logs.csv')
    parser.add_argument('--summary', required=True, help='Path to disposition_summary.csv')
    return parser.parse_args()



# DATA FUNCTIONS #

def load_data(roster_path, logs_path, summary_path):
    # Loading the csv files using pandas
    try:
        roster = pd.read_csv(roster_path)
        logs = pd.read_csv(logs_path)
        summary = pd.read_csv(summary_path)
        logging.info("Files loaded successfully.") # If file is loaded successfully
        return roster, logs, summary
    except Exception as e:
        logging.error(f"Error loading data: {e}") # If the file is missing or there is any problem in loading the file
        raise

def merge_data(roster, logs, summary):
    # This function performs the join operation
    # First 'call_logs.csv' is joined with 'disposition_summary.csv'
    # Second the dataset obtained by performing first join is then joined with 'agent_roster.csv'
    try:
        # JOIN 1 (on 'agent_id','org_id','call_date')
        merged = logs.merge(summary, on=['agent_id','org_id','call_date'], how='left')
        # JOIN 2 (on 'agent_id','org_id')
        full_data = merged.merge(roster, on=['agent_id','org_id'], how='left')
        logging.info("Data merged successfully.") # If JOIN operation is executed successfully 
        return full_data
    except Exception as e:
        logging.error(f"Error merging data: {e}") # If error occurs in JOIN operation
        raise



# PROCESSING

def generate_agent_summary(full_data):
    try:
        
        # Presence => 1 if login_time exists, else it will be 0
        full_data['presence'] = full_data['login_time'].notna().astype(int)

        # Calculating completed calls
        full_data['is_completed'] = full_data['status'] == 'completed'

        global summary
        # Grouping of the data by 'agent_id', 'users_first_name', 'users_last_name', 'call_date'
        # Then aggregation is done by adding columns 'total_calls','unique_loans_contacted','completed_calls','average_call_duration','presence'
        summary = full_data.groupby(
            ['agent_id', 'users_first_name', 'users_last_name', 'call_date'],
            as_index=False
        ).agg(
            total_calls=('call_id', 'count'),
            unique_loans_contacted=('installment_id', 'nunique'),
            completed_calls=('is_completed', 'sum'),
            avg_call_duration_min=('duration', lambda x: round(x.dropna().mean() / 60, 2)),
            presence=('presence', 'max')
        )
        # Calculating connect rate
        summary['Connect_Rate'] = round(summary['completed_calls'] / summary['total_calls'] * 100, 2)


        logging.info("Agent performance summary created.") # Final dataset is created
        return summary

    except Exception as e:
        logging.error(f"Error generating summary: {e}")
        raise
    
# MAIN # 

def main():
    
    setup_logging()
    args = parse_args()

    try:
        roster, logs, summary = load_data(args.roster, args.logs, args.summary)
        full_data = merge_data(roster, logs, summary)
        agent_summary = generate_agent_summary(full_data)

        # Saving the result of all agents in 'agent_performance_summary.csv'
        output_file = "agent_performance_summary.csv"
        agent_summary.to_csv(output_file, index=False)
        logging.info(f"Summary saved to {output_file}") # Summary saved
        

        # Generating Slack-style Summary Message 
        
        summary_date = '2025-04-28' # As only one date is available so directly 2025-04-28 is taken
        
        # Converting 'call_date' into datetime
        agent_summary['call_date'] = pd.to_datetime(agent_summary['call_date'], errors='coerce')

        summary_day = agent_summary[agent_summary['call_date'] == pd.to_datetime(summary_date)]

        if not summary_day.empty:
            top_agent = summary_day.loc[summary_day['Connect_Rate'].idxmax()] # Calculating Max. Connect Rate
            avg_duration = round(summary_day['avg_call_duration_min'].mean(), 2) # Calculating average call duration
            total_agents = summary_day.shape[0] # total no. of agents

            slack_msg = f"""
            Agent Summary for {summary_date}
            Top Performer: {top_agent['users_first_name']} {top_agent['users_last_name']} ({top_agent['Connect_Rate']}% connect rate)
            Total Active Agents: {total_agents}
            Average Duration: {avg_duration} min
            """
            print(slack_msg)
            logging.info("Slack-style summary generated.") 
        else:
            print(f"No agent data available for {summary_date}")
            logging.warning(f"No agent data available for {summary_date}")


    except Exception as e:
        logging.error(f"Script failed: {e}")




# START OF PROGRAM #

if __name__ == "__main__":
    main()



