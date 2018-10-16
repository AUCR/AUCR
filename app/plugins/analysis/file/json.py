"""AUCR analysis plugin json dict handler."""
# coding=utf-8


def flatten_dict(json_data):
    meta = {}
    meta["report"] = {}
    for item in json_data:
        if type(json_data[item]) is dict:
            for values in json_data[item]:
                if type(json_data[item][values]) is dict:
                    for second_values in json_data[item][values]:
                        if type(json_data[item][values][second_values]) is dict:
                            for third_values in json_data[item][values][second_values]:
                                if type(json_data[item][values][second_values][third_values])\
                                        is not list or dict or None:
                                    print(type(json_data[item][values][second_values][third_values]))
                                    debug_test = json_data[item][values][second_values][third_values]
                                    if debug_test:
                                        meta["report"][str(item + "." + values + "." + second_values + "." +
                                                           third_values)] = \
                                                str(json_data[item][values][second_values][third_values])
                        elif type(json_data[item][values][second_values]) is not list or None:
                            none_test = str(json_data[item][values][second_values])
                            if none_test:
                                meta["report"][str(item + "." + values + "." + second_values)] =\
                                    str(json_data[item][values][second_values])
                elif type(json_data[item][values]) is not list or None:
                    values_test = json_data[item][values]
                    if values_test and str(values_test) != "none":
                        meta["report"][str(item + "." + values)] = str(json_data[item][values])
        elif type(json_data[item]) is list:
            for list_items in json_data[item]:
                test_dict = list_items
                if type(test_dict) is str:
                    meta["report"][item] = test_dict
                else:
                    meta[item] = json_data[item]
        elif type(json_data[item]) is not list or None:
            test_item = json_data[item]
            if test_item and str(test_item) != "none":
                meta["report"][item] = json_data[item]
    return meta