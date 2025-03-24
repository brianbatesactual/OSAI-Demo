import csv
import os

def export_sentence_pairs(pairs, path='data/training'):
    os.makedirs(path, exist_ok=True)
    output_path = 'data/training/sentence_pairs.csv'
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['sentence1', 'sentence2', 'score'])
        for sent1, sent2, score in pairs:
            writer.writerow([sent1, sent2, score])
