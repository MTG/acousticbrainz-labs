create temp view abtemphighlevel as (
  select highlevel.id
     , highlevel.mbid
     , model.model
     , data->>'value' as value
     , data->>'probability' as probability
  from highlevel
  join highlevel_model on highlevel.id = highlevel_model.highlevel
  join model on highlevel_model.model = model.id
 where model.model in ('genre_dortmund', 'genre_rosamerica', 'genre_tzanetakis', 'genre_electronic',
                       'mood_acoustic', 'mood_aggressive', 'mood_electronic', 'mood_happy',
                       'voice_instrumental') limit 100;
);

\copy (select * from abtemphighlevel) to '2019-03-21-acousticbrainz-highlevel.csv' with csv header;