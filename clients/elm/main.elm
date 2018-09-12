import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http
import Json.Decode as Decode
import Url.Builder as Url



-- MAIN


main =
  Browser.element
    { init = init
    , update = update
    , subscriptions = subscriptions
    , view = view
    }



-- MODEL
type alias Model =
  { msg : String
  }


-- INIT
init : () -> (Model, Cmd Msg)
init _ =
  ( Model "not connected"
  , Cmd.none
  )


-- UPDATE
type AppAction
  = RequestHelloWord

type AppSrvMsg
  = HelloWord (Result Http.Error String)

type Msg
  = Action AppAction
  | SrvMsg AppSrvMsg

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of

    Action action ->
      case action of
        RequestHelloWord ->
          ( model
          , requestHelloWord 
          )

    SrvMsg srvMsg ->
      case srvMsg of
        HelloWord result ->
          case result of
            Ok srv_msg ->
              ( { model | msg = srv_msg}
              , Cmd.none
              )
            Err _ ->
              ( { model | msg = "Error when requesting Hello Word message from server" }
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
    [ h2 [] [ text model.msg]
    , button [ onClick (Action RequestHelloWord)] [ text "Test Server!" ]
    ]



-- HTTP


requestHelloWord : Cmd Msg
requestHelloWord =
  Http.send toMsgHelloWord (Http.get "http://localhost:5000" Decode.string)

toMsgHelloWord : Result Http.Error String -> Msg
toMsgHelloWord result =
  SrvMsg (HelloWord result)