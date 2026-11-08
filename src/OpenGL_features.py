def OpenGL_feat():
    vertex_shader = """
        #version 330
        in vec2 in_vert;
        in vec2 in_uv;
        out vec2 v_uv;
        void main() {
            gl_Position = vec4(in_vert, 0.0, 1.0);
            v_uv = in_uv;
        }
    """

    fragment_shader = """
        #version 330
        uniform sampler2D texture0;
        in vec2 v_uv;
        out vec4 f_color;

        void main() {
            // Optional: subtle CRT curve only applied to the text layer
            vec2 uv = v_uv * 2.0 - 1.0;
            float curvature = 0.05; 
            uv += uv * dot(uv, uv) * curvature;
            uv = uv * 0.5 + 0.5;

            // If outside the curved bounds, draw nothing (transparent)
            if (uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0) {
                f_color = vec4(0.0); 
                return;
            }

            // Get the base text pixel
            vec4 base_color = texture(texture0, uv);

            // Create a glow by sampling nearby pixels
            float offset = 0.000001;
            vec4 bloom = texture(texture0, uv + vec2(offset, 0.0)) +
                         texture(texture0, uv - vec2(offset, 0.0)) +
                         texture(texture0, uv + vec2(0.0, offset)) +
                         texture(texture0, uv - vec2(0.0, offset));
            
            bloom *= 0.25; // Average the surrounding samples

            // Combine the sharp base text with the soft bloom.
            // Because the FBO background is transparent (alpha 0), the glow naturally fades out.
            f_color = base_color + (bloom * 1.2);
        }
    """

    return vertex_shader, fragment_shader