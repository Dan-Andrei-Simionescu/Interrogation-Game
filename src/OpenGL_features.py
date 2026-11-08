def OpenGL_feat(self):
     # GL Shader
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

    # GL Shader for curved screen effect
    fragment_shader = """
        #version 330
        uniform sampler2D texture0;
        in vec2 v_uv;
        out vec4 f_color;

        void main() {
            // CRT curve effect
            vec2 uv = v_uv * 2.0 - 1.0;
            float curvature = 0.15; 
            uv += uv * dot(uv, uv) * curvature;
            uv = uv * 0.5 + 0.5;

            // Pixelized screen style
            float pixel_size = 0.001; 
            
            // Screen size
            vec2 resolution = vec2(1400.0, 1000.0); 
            
            // aproximate coordonates for rounded like pixels
            vec2 pixelated_uv = floor(uv * (resolution / pixel_size)) / (resolution / pixel_size);

            // check edges with distorted coords but draw pixelized coords
            if (uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0) {
                f_color = vec4(0.0, 0.0, 0.0, 1.0); // Margini negre
            } else {
                f_color = texture(texture0, pixelated_uv); // Aplicăm textura pixelată
                
                // Horizontal lines effect
                // float scanline = sin(uv.y * 800.0) * 0.04;
                // f_color.rgb -= scanline;
            }
        }
    """

    return vertex_shader, fragment_shader

    