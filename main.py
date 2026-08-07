'''Python Library'''
import os
'''Functions'''
import api_queries
import transformation


def main():
    api_key = os.getenv("STRIPE_API_KEY")
    if not api_key:
        raise RuntimeError("No API Key provided, please input using env vars.")

    stripe_data = api_queries.data_retrieval(api_key)

    formatted_data = transformation.transform(stripe_data, api_key)

    pooled_values = transformation.revenue_machine(formatted_data)

    print(pooled_values)

if __name__ == "__main__":
    main()