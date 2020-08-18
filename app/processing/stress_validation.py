import numpy as np


def process_acc(acc_values):
    prev_raw_acc = acc_values[0]
    summarized_accs = []
    prev_cumulated_acc = []
    for value in acc_values:
        summarized_acc = max(abs(value['x'] - prev_raw_acc['x']), abs(value['y'] - prev_raw_acc['y']),
                             abs(value['z'] - prev_raw_acc['z']))
        print('previous value')
        print(prev_raw_acc)
        prev_raw_acc = value
        summarized_accs.append(summarized_acc)
        print('summarized acc')
        print(summarized_accs)

        if len(prev_cumulated_acc) > 0:
            filtered_acc = prev_cumulated_acc[-1] * 0.9 + (sum(summarized_accs) / float(len(summarized_accs)) * 0.1)
        else:
            filtered_acc = sum(summarized_accs) / float(len(summarized_accs)) * 0.1
        prev_cumulated_acc.append(filtered_acc)
        print(prev_cumulated_acc)

    return prev_cumulated_acc


def detect_movement(acc_values: list, acc_threshold: float):
    cumulated_acc = process_acc(acc_values)
    print('mean acc')
    print(np.mean(cumulated_acc))
    if np.mean(cumulated_acc) >= acc_threshold:
        return True
    else:
        return False
