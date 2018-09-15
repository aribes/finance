import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http
import Json.Decode as Decode
import Json.Encode as Encode

import Common exposing (..)
import LoadCsv

-- MAIN

main =
  Browser.element
    { init = init
    , update = update
    , subscriptions = subscriptions
    , view = view
    }

-- INIT
init : () -> (Model, Cmd Msg)
init _ =
  ( Model "" "" ""
  , Cmd.none
  )

-- Main Update
-- Mainly a routing methog to other updates
-- I have a feeling that I could something better...
update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    -- LoadCSV Msg
    SelectRawDataFile filename ->
      LoadCsv.update msg model
    SendRawDataFile ->
      LoadCsv.update msg model
    RawDataFileLoading result ->
      LoadCsv.update msg model
    -- TODO: Server Resp / Errors
    _ ->
      ( model
      , Cmd.none
      )

-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model =
  Sub.none


-- VIEW
view : Model -> Html Msg
view model =
  div []
    [ h2 [] [ text "Welcome to finance UI"]
    , h3 [] [ text "All the features can be selected on the left sidebar"]
    , p [] [text ("LastAppError: " ++ model.lastAppError)]
    , p [] [text ("LastSrvMsg: " ++ model.lastAppError)]
    ]