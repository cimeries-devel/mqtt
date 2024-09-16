import threading


# # Create an Event for notifying main thread.
# callback_done = threading.Event()
#
#
# # Create a callback on_snapshot function to capture changes
# def on_snapshot(doc_snapshot, changes, read_time):
#     for doc in doc_snapshot:
#         print(f"Received document snapshot: {doc.id}")
#     callback_done.set()
#
#
# doc_ref = db.collection("cities").document("SF")
#
# # Watch the document
# doc_watch = doc_ref.on_snapshot(on_snapshot)
