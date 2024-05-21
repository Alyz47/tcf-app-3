from ml_model.category_classification import predict
# from ml_model.MIX_MATCH_GEMINI.mix_and_match import mix_and_match


def do_category_classification(listing_image):
    labels = {'Button_Up_Shirt': 'Button Up Shirt',
              'T_Shirt': 'T-shirt',
              'Polo_Shirt': 'Polo Shirt',
              'Shirts_And_Blouse': 'Blouse',
              'Tank_Top': 'Tank Top',
              'Jackets_And_Coats': 'Jackets And Coats',
              'Dress': 'Dress',
              'Skirt': 'Skirt',
              'Jeans': 'Jeans',
              'Pants': 'Pants',
              'Shorts': 'Shorts',
              'background': ''}
    extracted_res = {}
    is_extracted = True
    extracted_categories = predict(listing_image)
    print(f"Extraction Results: {extracted_categories}")

    if extracted_categories['detected_objects']:
        for obj in extracted_categories['detected_objects']:
            label = obj['label']
            confidence = obj['confidence']
            extracted_res[label] = confidence
    else:
        label = 'background'
        confidence = 0.0
        extracted_res[label] = confidence
        is_extracted = False
        print("No prediction returned from YOLOv8")

    if is_extracted:
        highest_conf_label = max(zip(
            extracted_res.values(),
            extracted_res.keys()))[1]
        # Get the sub-category with highest confidence score
        # Dict that contains sub-category naming that matches our db
        sub_category_extracted = labels[highest_conf_label]
        selected_subcat_score = extracted_res[highest_conf_label]
        results = {'label': sub_category_extracted, 'score': selected_subcat_score}
    else:
        sub_category_extracted = labels[next(iter(extracted_res.keys()))]
        selected_subcat_score = extracted_res[next(iter(extracted_res.keys()))]
        results = {'label': sub_category_extracted, 'score': selected_subcat_score}

    return results

