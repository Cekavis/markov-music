# markov-music

## branch v3 修改内容

*   支持了高阶 Markov Chain，可以在 `markov_chain.py` 内修改参数 `ORDER`。
*   音高和时长为一个整体作为 Markov Chain 的元素，所以时长不同的相同音高的音被认为是完全不同的。
*   时长上取整到 30ms，可以在 midi_parser.py 内修改。
*   修了 parser 名字冲突的问题。
*   改了 Parser 类中解析文件的逻辑，仅支持单声（多声会按照 midi 文件中 message 的顺序在保持原本时长的前提下转为一个单声的序列）