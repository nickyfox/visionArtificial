from tp2.hu_moments_generation import generate_hu_moments_file
from tp2.training_model import train_model
from tp2.view import predict_model

generate_hu_moments_file()
model = train_model()
predict_model(model)