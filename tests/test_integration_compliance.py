import os
import xml.etree.ElementTree as ET

def test_sitemap_txt_compliance():
    """
    Validates that sitemap.txt contains the newly added wazuh-detailed.html URL.
    This ensures that search engines can discover the detailed Wazuh SIEM/XDR guide.
    """
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sitemap_txt_path = os.path.join(workspace_root, 'sitemap.txt')

    assert os.path.exists(sitemap_txt_path), "sitemap.txt must exist at the workspace root"

    with open(sitemap_txt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    expected_url = "https://songketmail.github.io/aws-3tier-deployment-for-ai-infra/wazuh-detailed.html"
    assert expected_url in content, f"sitemap.txt should list the detailed Wazuh guide URL: {expected_url}"


def test_sitemap_xml_compliance():
    """
    Validates that sitemap.xml contains the newly added wazuh-detailed.html URL
    within its standard XML schema structures.
    """
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sitemap_xml_path = os.path.join(workspace_root, 'sitemap.xml')

    assert os.path.exists(sitemap_xml_path), "sitemap.xml must exist at the workspace root"

    # Parse XML and extract namespaces
    tree = ET.parse(sitemap_xml_path)
    root = tree.getroot()

    # The default namespace in our sitemap.xml is http://www.sitemaps.org/schemas/sitemap/0.9
    ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    urls = []
    for url_node in root.findall('ns:url', ns):
        loc_node = url_node.find('ns:loc', ns)
        if loc_node is not None:
            urls.append(loc_node.text.strip())

    expected_url = "https://songketmail.github.io/aws-3tier-deployment-for-ai-infra/wazuh-detailed.html"
    assert expected_url in urls, f"sitemap.xml should contain the detailed Wazuh guide URL: {expected_url}"


def test_jekyll_config_navbar_compliance():
    """
    Validates that docs/_config.yml has properly registered /wazuh-detailed.html
    within the Jekyll site sidebar navigation settings.
    """
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    config_path = os.path.join(workspace_root, 'docs', '_config.yml')

    assert os.path.exists(config_path), "docs/_config.yml must exist"

    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verify that the URL is registered in the configuration
    assert "url: \"/wazuh-detailed.html\"" in content or "url: '/wazuh-detailed.html'" in content or "url: /wazuh-detailed.html" in content, \
        "docs/_config.yml must include /wazuh-detailed.html in its navbar configuration"


def test_jules_knowledge_ledger_completeness():
    """
    Validates that the Google Jules Master Knowledge Ledger (.agents/brain/jules_knowledge_ledger.md)
    exists and completely indexes all 51 distinct items of Jules knowledge from Day 0 until now.
    """
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    ledger_path = os.path.join(workspace_root, '.agents', 'brain', 'jules_knowledge_ledger.md')

    assert os.path.exists(ledger_path), "Google Jules Master Knowledge Ledger must exist under .agents/brain/"

    with open(ledger_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verify that all 51 knowledge items are indexed (IDs 1 to 51)
    for i in range(1, 52):
        expected_id_pattern = f"| **{i}** |"
        assert expected_id_pattern in content, f"Ledger must index knowledge item ID: {i}"
