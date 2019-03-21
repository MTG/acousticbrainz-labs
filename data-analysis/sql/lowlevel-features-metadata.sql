create temp view abtempdata as (
select ll.id,
       ll.gid as recording_mbid,
       ll.lossless,
       llj.data->'metadata'->'audio_properties'->>'codec' as codec,
       llj.data->'metadata'->'audio_properties'->>'bit_rate' as bit_rate,
       llj.data->'metadata'->'audio_properties'->>'sample_rate' as sample_rate,
       llj.data->'metadata'->'audio_properties'->>'length' as length,
       llj.data->'metadata'->'audio_properties'->>'replay_gain' as replay_gain,
       llj.data->'metadata'->'audio_properties'->>'md5_encoded' as md5_encoded,

       llj.data->'metadata'->'tags'->'title'->>0 as recording,
       llj.data->'metadata'->'tags'->'artist'->>0 as artist,
       llj.data->'metadata'->'tags'->'musicbrainz_artistid'->>0 as artist_mbid,
       llj.data->'metadata'->'tags'->'album'->>0 as release,
       llj.data->'metadata'->'tags'->'musicbrainz_albumid'->>0 as release_mbid,
       llj.data->'metadata'->'tags'->'genre'->>0 as genre,

       llj.data->'metadata'->'tags'->'date'->>0 as date,
       llj.data->'metadata'->'tags'->'originaldate'->>0 as originaldate,

       llj.data->'tonal'->>'key_key' as key_key,
       llj.data->'tonal'->>'key_scale' as key_scale,

       llj.data->'tonal'->>'tuning_frequency' as tuning_frequency,
       llj.data->'tonal'->>'tuning_equal_tempered_deviation' as tuning_equal_tempered_deviation,

       llj.data->'lowlevel'->>'average_loudness' as average_loudness,
       llj.data->'lowlevel'->>'dynamic_complexity' as dynamic_complexity,
       llj.data->'lowlevel'->'mfcc'->'mean'->>0 as mfcc_zero_mean,

       llj.data->'rhythm'->>'bpm' as bpm,
       llj.data->'rhythm'->'bpm_histogram_first_peak_bpm'->>'mean' as bpm_histogram_first_peak_bpm_mean,
       llj.data->'rhythm'->'bpm_histogram_first_peak_bpm'->>'median' as bpm_histogram_first_peak_bpm_median,
       llj.data->'rhythm'->'bpm_histogram_second_peak_bpm'->>'mean' as bpm_histogram_second_peak_bpm_mean,
       llj.data->'rhythm'->'bpm_histogram_second_peak_bpm'->>'median' as bpm_histogram_second_peak_bpm_median,
       llj.data->'rhythm'->>'danceability' as danceability,
       llj.data->'rhythm'->>'onset_rate' as onset_rate

       from lowlevel as ll,
      lowlevel_json as llj
    where ll.id = llj.id);

\copy (select * from abtempdata) to '2019-03-21-acousticbrainz-features-metadata.csv' with csv header;
