%% erlang-pre-commit のフック検証用モジュール
-module(fixture_app).

-export([add/2, reverse/1]).


-spec add(integer(), integer()) -> integer().
add(Left, Right) ->
    Left + Right.


-spec reverse([T]) -> [T].
reverse(List) ->
    lists:reverse(List).
