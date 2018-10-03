module LoadCsv exposing (update, view)

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http
import Json.Encode as Encode
import Json.Decode as Decode

import Common exposing (..)

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    SelectRawDataFile filename ->
      ( { model | fileSelected = filename }
      , Cmd.none 
      )
    SendRawDataFile ->
      ( model
      , sendRawDataFile model
      )
    RawDataFileLoading result ->
      case result of
        Ok srv_msg ->
          ( { model | lastSrvMsg = srv_msg}
          , Cmd.none
          )
        Err _ ->
          ( { model | lastSrvMsg = "Error when sending raw data file" }
          , Cmd.none
          )
    _ ->
      (
        { model | lastAppError = "Routing error in LoadCsv"}
        , Cmd.none
      )

sendRawDataFile : Model -> Cmd Msg
sendRawDataFile model =
  Http.send RawDataFileLoading (
    Http.post "http://localhost:5000/load" (Http.jsonBody (Encode.string model.fileSelected)) Decode.string)

view : Model -> Html Msg
view model =
  div []
    [ h2 [] [ text model.fileSelected]
    , button [ onClick SendRawDataFile ]  [ text "Upload RawDataFile" ]
    , input [attribute "type" "file", onInput SelectRawDataFile ] []
    ]