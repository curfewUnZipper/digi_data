import tensorflow as tf
import tf2onnx

model = tf.keras.models.load_model("lstm_model.h5", compile=False)

model.output_names = ["output"]
input_signature = [tf.TensorSpec(model.inputs[0].shape, tf.float32, name="input")]

onnx_model, _ = tf2onnx.convert.from_keras(model, input_signature=input_signature)

with open("lstm_model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())
