CREATE or replace VIEW aion_analytics.view_tool_events as (
select te.id, te.timestamp,t.name as tool, ten.name AS event, tc.name as classification from
  aion_analytics.tool_event as te
  LEFT JOIN aion_analytics.tool_event_name ten on te.event=ten.id
  LEFT JOIN aion_analytics.tool t on te.tool=t.id
  LEFT join aion_analytics.tool_has_classification thc on te.tool = thc.tool
  inner join aion_analytics.tool_classification tc on thc.classification=tc.id
)