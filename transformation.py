import json
import warnings
import api_queries

def transform(stripe_data: list, key: str):
    formatted_list = []
    for payment in stripe_data:
        if payment["status"] == "succeeded" and payment["amount_received"] != 0:
            charge_id = payment["latest_charge"]
            stripe_fee = api_queries.fee_retrieval(charge_id, key)
            formatted_list.append({
                "machine": payment["metadata"].get("station_id"),
                "amount": payment["amount_received"],
                "stripe_fee": stripe_fee,
                "net_amount": payment["amount_received"] - stripe_fee
            })
        else:
           warnings.warn
           (f"{payment['metadata'].get('station_id')} is cancelled, not appending to revenue sheet."),
           RuntimeWarning

    return formatted_list


def revenue_machine(json_body: list):
    machine_pool = {}
    
    for value in json_body:
        machine_name = value["machine"]
        machine_amount = value["net_amount"]
        if machine_name not in machine_pool:
            machine_pool[machine_name] = 0

        machine_pool[machine_name] += machine_amount

    total_net_amount = sum(machine_pool.values())
    machine_pool["total_net_amount"] = total_net_amount
    
    json_output = json.dumps(machine_pool, indent=2)
    return json_output