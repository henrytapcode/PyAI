# Chaining layers with `nn.Sequential`

Instead of storing each layer in its own attribute (`self.hidden`, `self.relu`, `self.out`) and calling them one by one inside `forward`, this alternative packs the linear-ReLU-linear stack into a single `nn.Sequential` container. `nn.Sequential` is cleaner and less repetitive whenever data flows strictly straight through a list of layers with no branches. Write an explicit `forward` method whenever a model needs skip connections, multiple inputs or outputs, or conditional routing between layers.
