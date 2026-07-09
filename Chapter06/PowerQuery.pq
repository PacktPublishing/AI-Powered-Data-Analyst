-- Power Query: truncate timestamp precision before load 
-- Reduces cardinality from ~86,400 unique values/day to ~1,440 
= Table.TransformColumns( 
   Source, 
   {{"event_timestamp", each DateTime.From(DateTime.ToText(_, "yyyy-MM-dd HH:mm")), type datetime}} 
) 
 
-- Power Query: remove unused columns before load 
-- Never import columns you do not use in measures or visuals 
= Table.RemoveColumns(Source, {"internal_notes", "legacy_id", "raw_payload"}) 
