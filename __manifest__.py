# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'WEHA - Smart Pos',
    'summary': """Smart Point of Sale""",
    'version': '14.0.0.1.0',
    'license': 'AGPL-3',
    'category': 'Point of sale',
    'author': 'WEHA',
    'website': 'https://www.weha-id.com',
    'depends': ['base'],
    'data': [
        'data/weha_smart_pos_data.xml',
        'security/weha_smart_pos_security.xml',
        'views/weha_smart_post_templates.xml'
    ],
    'application': True,
    'installable': True,
    "auto_install": False,
}
