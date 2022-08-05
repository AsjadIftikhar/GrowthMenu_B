def status_change(new_sub_status):
    MAPPINGS = {
        'In Progress': 'Active',
        'Awaiting Brief': 'Active',
        'In Revision': 'Active',
        'Complete': 'Completed',
        'Refund': 'Refunded',
        'Canceled': 'Canceled'
    }
    new_status = MAPPINGS.get(new_sub_status)
    return new_status
