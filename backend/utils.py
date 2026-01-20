import json
import polars as pl

def test_concat(df: pl.DataFrame) -> pl.DataFrame:
    row = pl.DataFrame({"name": ["test"], "date": [None], "message": ["test"], "isPhoto": [False], "reactions": [[]]})
    print("Test row to add")
    print(df)
    return pl.concat([df, row])

def fix_encoding(text):
    if text is None:
        return None
    try:
        # Facebook sometimes double-encodes as latin1
        return text.encode('latin1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError, AttributeError):
        return text
    
def parseJsonMessagesToDf(messages: list) -> pl.DataFrame:
    for msg in messages:
        if msg.get("content"):
            msg["content"] = fix_encoding(msg["content"])
    df_part = pl.DataFrame(messages).with_columns(pl.col("sender_name").alias("name"),
                                             pl.from_epoch("timestamp_ms", time_unit="ms").alias("date"),
                                             pl.col("content").alias("message"),
                                             ).select("name", "date", "message")
    print(df_part)
    return df_part

def getTopMessages(df: pl.DataFrame, username: str, n: int) -> pl.DataFrame:
    first_name =""
    try:
        first_name = username.split(" ")[0]
    except Exception as e:
        print(str(e))
    print(username, first_name)
    message_groups = df.filter(pl.col("name") == username, 
                               pl.col("message") != "None", 
                               pl.col("message") != first_name + " sent an attachment.",
                               pl.col("message") != "You sent an attachment.",
                               pl.col("message") != "Audio call ended",
                               pl.col("message") != "Liked a message"
                               ).group_by("message").agg(pl.len()).sort("len", descending=True)
    i = 0
    for row in message_groups.iter_rows():
        print(row)
        i += 1
        if i == n:
            break
    
    return message_groups.head(n)

def getLongestMessages(df: pl.DataFrame, username: str, n: int) -> pl.DataFrame:
    longest_messages = df.filter(pl.col("name") == username).group_by("message").agg(pl.col("message").str.len_chars().alias("len")).sort("len", descending=True)
    return longest_messages.head(n)

def main():
    print("For testing")

if __name__ == "__main__":
    main()
