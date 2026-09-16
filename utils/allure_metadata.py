

def get_allure_metadata(item):
    metadata = {
        "epic": None,
        "feature": None,
        "story": None,
        "description": None,
    }

    for marker in item.iter_markers("allure_label"):
        label_type = marker.kwargs.get("label_type")

        if label_type in {"epic", "feature", "story"}:
            if marker.args:
                metadata[label_type] = marker.args[0]

    description_marker = next(
        item.iter_markers("allure_description"),
        None,
    )

    if description_marker and description_marker.args:
        metadata["description"] = description_marker.args[0]

    return metadata

