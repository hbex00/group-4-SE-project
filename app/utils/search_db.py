from flask import Flask, session
from sqlalchemy import select, String, Text, or_
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.inspection import inspect
from app.services.models import Tag
from database.db import db


def text_search_table(pattern,orm_class,class_tags=None):
    if not pattern:
        pattern = ""
    
    if not orm_class:
        raise ValueError("Empty class")
    
    if not isinstance(orm_class, DeclarativeMeta):
        raise TypeError("orm_class must be a SQLAlchemy model")

    search_pattern  
    if pattern == "":
        search_pattern = f"%"
    else:
        search_pattern = f"%{pattern}%"  

    table_text_columns = []
    for column in orm_class.__table__.columns:
        if isinstance(column.type, (String,Text)):
            table_text_columns.append(column)
    if not table_text_columns:
        return []

    column_match_conditions = [column.ilike(search_pattern) for column in table_text_columns]
    matching_table_query = select(orm_class).where(or_(*column_match_conditions))

    if class_tags:
        class_category, class_units = class_tags
        orm_class_tag: DeclarativeMeta = None
        mapper = inspect(orm_class)

        for relation in mapper.relationships:
            target = relation.entity.class_
            if hasattr(target,"tag_id"):
                orm_class_tag = target
                break

        if orm_class_tag is None:
            raise ValueError("No tags found for " + str(orm_class))

        # essentially a query/function to explore in-depth and return foreign keys in an SQL Orm class
        parent_foreign_key = next(column
                                  for column in orm_class_tag.__table__.columns
                                    if column.foreign_keys and any(
                                        fk.column.table == orm_class.__table__
                                        for fk in column.foreign_keys))
        
        matching_table_query = (matching_table_query
                                .join(orm_class_tag, parent_foreign_key==orm_class.id)
                                .join(Tag,Tag.id == orm_class_tag.tag_id)
                                .where(Tag.category == class_category,Tag.unit.in_(class_units))
                                .group_by(orm_class.id)
                                .distinct())

    try:
        return db.session.execute(matching_table_query).scalars().all()
    except: raise