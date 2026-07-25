def apply_corrections(entities, corrections):
    for entity in entities:
    
        id = entity.id

        if id in corrections:
            entity.update(corrections[id])
        
    return entities