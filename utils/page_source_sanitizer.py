import xml.etree.ElementTree as ET


KEEP_ATTRIBUTES = {
    "resource-id",
    "text",
    "content-desc",
    "class",
    "package",
    "clickable",
    "enabled",
    "displayed",
    "focused",
    "selected",
}

DEFAULT_MAX_LENGTH = 8000


def sanitize_page_source(page_source: str, max_length: int = DEFAULT_MAX_LENGTH) -> str:
    """
    Sanitizes an Appium Android UI hierarchy XML document for diagnostics.

    Keeps attributes that are useful for mobile failure analysis while removing
    noisy attributes that add little diagnostic value. The resulting XML is
    truncated to the requested maximum length.
    """
    if not page_source:
        return ""

    try:
        root = ET.fromstring(page_source)
    except ET.ParseError:
        return page_source[:max_length]

    for element in root.iter():
        element.attrib = {
            name: value
            for name, value in element.attrib.items()
            if name in KEEP_ATTRIBUTES
        }

        if element.text:
            element.text = " ".join(element.text.split())

        if element.tail:
            element.tail = None

    sanitized = ET.tostring(root, encoding="unicode")
    return sanitized[:max_length]
