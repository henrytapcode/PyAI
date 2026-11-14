# Mini-batch DataLoader fine-tuning

Instead of running one full-batch step per epoch over all training tickets, this alternative wraps the tokenized tensors in a `TensorDataset` and iterates with `DataLoader(..., batch_size=8, shuffle=True, num_workers=0, generator=...)`, updating weights once per mini-batch and returning the average batch loss per epoch.

Mini-batching uses much less memory and takes more optimizer steps per epoch when datasets grow beyond a few dozen examples, while full-batch training in `solution.py` is simpler and fast enough for tiny CPU datasets.
