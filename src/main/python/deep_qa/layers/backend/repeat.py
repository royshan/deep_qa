from keras import backend as K
from keras.layers import Layer
from overrides import overrides


class Repeat(Layer):
    """
    This `Layer` calls `K.repeat_elements` on both the input and the mask, after calling
    `K.expand_dims`.

    If the mask is not `None`, we must be able to call `K.expand_dims` using the same axis
    parameter as we do for the input.

    Input:
        - A tensor of arbitrary shape.

    Output:
        - The input tensor repeated along one of the dimensions.
    """
    def __init__(self, axis: int, repetitions: int, **kwargs):
        self.supports_masking = True
        self.axis = axis
        self.repetitions = repetitions
        super(Repeat, self).__init__(**kwargs)

    @overrides
    def compute_mask(self, inputs, mask=None):
        # pylint: disable=unused-argument
        if mask is None:
            return None
        return K.repeat_elements(K.expand_dims(mask, self.axis), self.repetitions, self.axis)

    @overrides
    def get_output_shape_for(self, input_shape):
        return input_shape[:self.axis] + (self.repetitions,) + input_shape[self.axis:]

    @overrides
    def call(self, x, mask=None):
        return K.repeat_elements(K.expand_dims(x, self.axis), self.repetitions, self.axis)
