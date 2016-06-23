import ab_pb2
import json
import sys
# Making the json schema for the song features

song_feature_types = {"lowlevel" : {
                     "average_loudness"        : float,
                     "barkbands_crest"         : "statistics",
                     "barkbands_kurtosis"      : "statistics",
                     "barkbands_flatness_db"   : "statistics",
                     "barkbands_skewness"      : "statistics",
                     "barkbands_spread"        : "statistics",
                     "dissonance"              : "statistics",
                     "dynamic_complexity"       : float,
                     "erbbands_crest"          : "statistics",
                     "erbbands_flatness_db"    : "statistics",
                     "erbbands_kurtosis"       : "statistics",
                     "erbbands_skewness"       : "statistics",
                     "erbbands_spread"         : "statistics",
                     "hfc"                     : "statistics",
                     "melbands_crest"          : "statistics",
                     "melbands_flatness_db"    : "statistics",
                     "melbands_kurtosis"       : "statistics",
                     "melbands_skewness"       : "statistics",
                     "melbands_spread"         : "statistics",
                     "pitch_salience"          : "statistics",
                     "silence_rate_20dB"       : "statistics",
                     "silence_rate_30dB"       : "statistics",
                     "silence_rate_60dB"       : "statistics",
                     "spectral_centroid"       : "statistics",
                     "spectral_complexity"     : "statistics",
                     "spectral_decrease"       : "statistics",
                     "spectral_energy"         : "statistics",
                     "spectral_energyband_high": "statistics",
                     "spectral_energyband_low" : "statistics",
                     "spectral_energyband_middle_high" : "statistics",
                     "spectral_energyband_middle_low" : "statistics",
                     "spectral_entropy" : "statistics",
                     "spectral_flux"           : "statistics",
                     "spectral_kurtosis"       : "statistics",
                     "spectral_rms"            : "statistics",
                     "spectral_rolloff"        : "statistics",
                     "spectral_skewness"       : "statistics",
                     "spectral_spread"         : "statistics",
                     "spectral_strongpeak"     : "statistics",
                     "zerocrossingrate"        : "statistics",
                     "barkbands"               : "detailed_statistics",
                     "erbbands"                : "detailed_statistics",
                     "gfcc"                    : "cov_statistics",
                     "melbands"                : "detailed_statistics",
                     "mfcc"                    : "cov_statistics",
                     "spectral_contrast_coeffs": "detailed_statistics", 
                     "spectral_contrast_valleys": "detailed_statistics",
           
                 }, 
                 "metadata" : {
                     "audio_properties" : {
                         "analysis_sample_rate" : int,
                         "bit_rate"              : int,
                         "equal_loudness"       : int,
                         "length"               : float,
                         "lossless"             : int,
                         "replay_gain"          : float,
                         "sample_rate"          : int,
                         "codec"                : str,
                         "downmix"              : str,
                         "md5_encoded"          : str,
                     },
                     "tags"             : {
                         "file_name"             : str,
                         "album"                : str,
                         "albumartist"          : str,
                         "albumartistsort"      : str,
                         "artist"               : str,
                         "artistsort"           : str,
                         "date"                 : str,
                         "discnumber"           : str,
                         "encoding"             : str,
                         "label"                : str,
                         "media"                : str,
                         "musicbrainz_album_release_country" : str,
                         "musicbrainz_album_status"          : str,
                         "musicbrainz_album_type" : str,
                         "musicbrainz_albumartistid" : str,
                         "musicbrainz_albumid"  : str,
                         "musicbrainz_artistid" : str,
                         "musicbrainz_releasegroupid" : str,
                         "musicbrainz_trackid"  : str,
                         "originaldate"         : str,
                         "script"               : str,
                         "title"                : str,
                         "tracknumber"          : str
                     },
                     "version"        : {
                         "essentia"             : str,
                         "essentia_build_sha"     : str,
                         "essentia_git_sha"     : str,
                         "extractor"            : str
                     }
                 }, 
                 "tonal"    : {
                     "chords_changes_rate" : float,
                     "chords_number_rate"  : float,
                     "chords_strength"     : "statistics",
                     "hpcp_entropy"        : "statistics",
                     "key_strength"        : float,
                     "tuning_diatonic_strength" : float,
                     "tuning_equal_tempered_deviation" : float,
                     "tuning_frequency"    : float,
                     "tuning_nontempered_energy_ratio" : float,
                     "hpcp"                : "detailed_statistics",
                     "chords_histogram"    : "list_of_doubles",
                     "thpcp"               : "list_of_doubles",
                     "chords_key"          : str,
                     "chords_scale"        : str,
                     "key_key"             : str,
                     "key_scale"           : str
                 }, 
                 "rhythm"   : {
                     "beats_count"          : int,
                     "beats_loudness"       : "statistics",
                     "bpm"                  : float,
                     "bpm_histogram_first_peak_bpm" : "statistics",
                     "bpm_histogram_first_peak_spread" : "statistics",
                     "bpm_histogram_first_peak_weight" : "statistics",
                     "bpm_histogram_second_peak_bpm"   : "statistics",
                     "bpm_histogram_second_peak_spread": "statistics",
                     "bpm_histogram_second_peak_weight": "statistics",
                     "danceability"                    : float,
                     "onset_rate"                      : float,
                     "beats_loudness_band_ratio"       : "detailed_statistics",
                     "beats_position"                  : "list_of_doubles"
                 }
                }
additional_types = {
    "statistics" : {
        "dmean"   : float,
        "dmean2"  : float,
        "dvar"    : float,
        "dvar2"   : float,
        "max"     : float,
        "mean"    : float,
        "median"  : float,
        "min"     : float,
        "var"     : float
    },

    "detailed_statistics" : {
        "dmean"   : list,
        "dmean2"  : list,
        "dvar"    : list,
        "dvar2"   : list,
        "max"     : list,
        "mean"    : list,
        "median"  : list,
        "min"     : list,
        "var"     : list   
    },  

    "cov_statistics" : {
        "mean"      : list,
        "cov"       : "list of lists",
        "icov"      : "list of lists"
    },

    "list_of_lists" : [[]],
    "list_of_doubles":[]
}

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

if __name__=="__main__":
    filename = sys.argv[1]
    json_data = open(filename).read()
    data = json.loads(json_data)
    data = convert(data)
    song_details = ab_pb2.song_features()

    for feature_set in data:
        print(feature_set)

        if(type(data[feature_set])==dict):

            for feature_description in data[feature_set]:
                print("        " + feature_description)

                if type(song_feature_types[feature_set][feature_description]) == type(float) :
                    this_field_type = song_feature_types[feature_set][feature_description]
                    if this_field_type == float:
                        exec("song_details.%s.%s = %f" % (feature_set, feature_description, float(data[feature_set][feature_description])))
                    elif this_field_type == str:
                        pass
                        x = data[feature_set][feature_description]
                        exec("song_details.%s.%s = '%s'" % (feature_set, feature_description, x))
                    elif this_field_type == int:
                        exec("song_details.%s.%s = %d" % (feature_set, feature_description, int(data[feature_set][feature_description])))

                elif type(song_feature_types[feature_set][feature_description]) == dict:
                    for feature_attribute in data[feature_set][feature_description]:
                        data_type = song_feature_types[feature_set][feature_description][feature_attribute.replace(" ","_")]
                        data_value = data_type(data[feature_set][feature_description][feature_attribute])
                        feature_attribute = feature_attribute.replace(" ","_")
                        if data_type == float:
                            exec("song_details.%s.%s.%s = %f" % (feature_set, feature_description, feature_attribute, data_value))
                        elif data_type == str:
                            pass
                            exec('song_details.%s.%s.%s = "%s"' % (feature_set, feature_description, feature_attribute, str(data_value)))

                        elif data_type == int:
                            exec("song_details.%s.%s.%s = %d" % (feature_set, feature_description, feature_attribute, data_value))

                else:
                    this_field_type = song_feature_types[feature_set][feature_description]
                    if type(additional_types[this_field_type]) == dict:
                        for feature_attribute in data[feature_set][feature_description]:
                            data_value = data[feature_set][feature_description][feature_attribute]
                            feature_attribute = feature_attribute.replace(" ","_")
                            data_type = additional_types[this_field_type][feature_attribute]
                            if data_type == float:
                                exec("song_details.%s.%s.%s = %f" % (feature_set, feature_description, feature_attribute, data_type(data_value)))
                            elif data_type == str:
                                pass
                                exec("song_details.%s.%s.%s = '%s'" % (feature_set, feature_description, feature_attribute, data_value))
                            elif data_type == int:
                                exec("song_details.%s.%s.%s = %d" % (feature_set, feature_description, feature_attribute, data_type(data_value)))
                            elif data_type == list:
                                exec("song_details.%s.%s.%s.extend(%s)" % (feature_set, feature_description, feature_attribute, data_type(data_value)))
                            else:
                                for sub_list in list(data_value):
                                     temp_list_of_doubles = ab_pb2.list_of_doubles()
                                     temp_list_of_doubles.value.extend(list(sub_list))    
                                     exec("song_details.%s.%s.%s.nested_list.add().value.extend(list(%s))" % (feature_set, feature_description, feature_attribute, sub_list))

    protobuf_string = song_details.SerializeToString()        
    f = open("output.protobuf","w")
    f.write(protobuf_string)
    f.close()  
