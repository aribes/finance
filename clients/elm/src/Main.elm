import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http
import Json.Decode as Decode
import Json.Encode as Encode

import Common exposing (..)
import LoadCsv

import Element
import Element.Font as Font

main =
  Browser.element
    { init = init
    , update = update
    , subscriptions = subscriptions
    , view = view
    }

-- Rmk - could call a specific method in Common
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
  Element.layout []
    <| Element.column [] [
       (Element.row [] [Element.el [Font.size 32] (Element.text "Welcome to finance UI")])
      ,(Element.row [] [Element.el [Font.size 24] (Element.text "All the features can be selected on the left sidebar")])
      ,(Element.row [] [Element.el [Font.size 14] (Element.text ("LastAppError: " ++ model.lastAppError))])
      ,(Element.row [] [Element.el [Font.size 14] (Element.text ("LastSrvMsg: " ++ model.lastSrvMsg))])
    ]