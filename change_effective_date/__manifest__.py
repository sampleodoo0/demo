{
    'name': 'Effective Date Change',
    'description': 'change_effective_date',
    'version': '16.0.1.0.0',
    'application': True,
    'depends': [
        'base',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/effective_date _groups.xml',
        'views/wizard_effective_date.xml'
    ],
}
