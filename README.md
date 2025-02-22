# golden_apple
The multimodal agent for giving investment advice on apple products based on a complex set of events.

The way it works is
1) The API call to the chatGPT/Perplexity (or other GenAI) in order to get the major events in a specific time frame. (preprocessing).
2) Mapping the set of events to the specific snippets of the financial data that showcases the general change in prices. (preprocessing).
3) Predictor of the price trend based on the provided events (sounds like a generative model that will generate the overall trend based off of the prices).

Those are the three stages/models.
