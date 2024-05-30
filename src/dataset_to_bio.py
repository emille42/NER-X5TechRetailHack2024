"""
Набор функция для перевода датасета в формат BIO
"""

def dataset_to_text_with_labels(dataset):
    dataset_texts = []
    dataset_labels = []

    for sample in dataset:
        text = sample["text"]
        entities = sample["entities"]

        last_end = 0

        splitted_text = []
        text_labels = []
        for entity in entities:
            entity_label = entity["entity_group"]
            entity_start = entity["start"]
            entity_end = entity["end"]

            previous_part = text[last_end:entity_start]
            entity_part = text[entity_start:entity_end]
            # entity_part = entity["word"]
            
            last_end = entity_end
            if len(previous_part) > 0:

                splitted_text.append(previous_part)
                text_labels.append("O")

            splitted_text.append(entity_part)
            text_labels.append(entity_label)

        last_text_part = text[last_end:]
        if len(last_text_part) > 0:
            splitted_text.append(last_text_part)
            text_labels.append("O")
        
        dataset_texts.append(splitted_text)
        dataset_labels.append(text_labels)

    return dataset_texts, dataset_labels



def process_tokens(tokens):
    tokens = tokens.split(" ")
    tokens = list(filter(None, tokens))
    return tokens

def texts_labels_to_bio(dataset_texts, dataset_labels):
    dataset_processed = []
    dataset_bio = []

    for texts, labels in zip(dataset_texts, dataset_labels):
        processed_sample = []
        sample_bio_labels = []
        for fragment, label in zip(texts, labels):
            tokens = process_tokens(fragment)
            processed_sample += tokens
            
            if label == "O":
                for _ in range(len(tokens)):
                    sample_bio_labels.append("O")
            else:
                for i in range(len(tokens)):
                    if i == 0:
                        sample_bio_labels.append("B-" + label)
                    else:
                        sample_bio_labels.append("I-" + label)

        dataset_processed.append(processed_sample)
        dataset_bio.append(sample_bio_labels)

    return dataset_processed, dataset_bio



def labels_to_id(labels, labels2id):
    result = []

    for sample in labels:
        sample_id_labels = []
        for label in sample:
            sample_id_labels.append(labels2id[label])
        result.append(sample_id_labels)
        
    return result