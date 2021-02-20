# study-python-wsjsonrpc

Pythonによる、WebSocket上で動作する双方向JSON-RPCの実装実験。

## 要件

+ メソッド名にピリオドを含めて階層化したい。
+ 引数は配列ではなくオブジェクトとしたい。
+ 双方向にメソッドを呼び出したい。
+ サーバー側に終了メソッドを用意したい。

## 結果

[wsjsonrpc](https://pypi.org/project/wsjsonrpc/)を利用することで目的を達成することを確認できた。

[jsonrpcserver](https://github.com/bcb/jsonrpcserver)のほうが構造的にモダンだが、jsonrpcserverは双方向のメソッド呼び出しが困難であり、再実装が必要と思われる。
