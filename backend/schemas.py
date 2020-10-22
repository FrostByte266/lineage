from flask_marshmallow import Marshmallow

from models import Timeline, TimelineNode

ma = Marshmallow()

class TimelineNodeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TimelineNode
        include_fk = True

timeline_nodes_schema = TimelineNodeSchema(many=True)
timeline_node_schema = TimelineNodeSchema(many=False)

class TimelineSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Timeline
        include_fk = True

    nodes = ma.Nested(TimelineNodeSchema, many=True)

timelines_schema = TimelineSchema(many=True)
timeline_schema = TimelineSchema(many=False)
