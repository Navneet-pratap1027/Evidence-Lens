import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from app.services.rag_service import chunk_text, rank_chunks


article = """
NPCI has confirmed that UPI services continue to operate normally across India.
There is no ban on UPI payments.
Banks continue to process UPI transactions.
The viral social media claim is false.
""" * 100

claim = "UPI payments have been banned across India"

chunks = chunk_text(article)

results = rank_chunks(claim, chunks)

print("=" * 80)

for item in results:

    print("Similarity:", item["similarity"])

    print(item["text"][:250])

    print("-" * 80)