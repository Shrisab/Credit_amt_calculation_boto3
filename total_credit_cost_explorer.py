import boto3
from datetime import datetime, timedelta

def get_total_credit_amount():
    try:
        # Initialize Cost Explorer client
        client = boto3.client('ce', region_name='us-east-1')

        # Define the time period for which you want to retrieve credits
        end = datetime.utcnow().date()
        start = end - timedelta(days=30)  # Last 30 days, adjust as needed

        total_credit = 0.0
        next_token = None

        # Iterate through pages of results
        while True:
            # Prepare request parameters
            request_params = {
                'TimePeriod': {
                    'Start': start.strftime('%Y-%m-%d'),
                    'End': end.strftime('%Y-%m-%d')
                },
                'Granularity': 'MONTHLY',
                'Metrics': ['UnblendedCost'],
                'Filter': {
                    'And': [
                        {'Dimensions': {'Key': 'RECORD_TYPE', 'Values': ['Credit']}},
                        {'Dimensions': {'Key': 'SERVICE', 'Values': ['Total']}}  # Filter by Total service to exclude other services
                    ]
                }
            }

            if next_token:
                request_params['NextPageToken'] = next_token

            # Query Cost Explorer for credits
            response = client.get_cost_and_usage(**request_params)

            # Process results
            results = response['ResultsByTime']
            for result in results:
                total_credit += float(result['Total']['UnblendedCost']['Amount'])

            # Check for pagination
            next_token = response.get('NextPageToken')
            if not next_token:
                break

        return total_credit

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Calculate and print the total credit amount
total_credit_amount = get_total_credit_amount()

if total_credit_amount is not None:
    print(f"The total credit amount is: ${total_credit_amount:.2f}")
