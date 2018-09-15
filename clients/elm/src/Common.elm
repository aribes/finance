module Common exposing (..)

import Http

-- CSV Part of the model
type alias Model =
  { lastAppError : String
  , lastSrvMsg : String
  , fileSelected : String
  }

type Msg
  -- Generic message from Srv interaction
  -- String is the "page" that has sent the request
  = ServerError String (Result Http.Error String)
  | ServerResp String String
  -- CSV Part of the Msg
  | SelectRawDataFile String
  | SendRawDataFile
  | RawDataFileLoading (Result Http.Error String)