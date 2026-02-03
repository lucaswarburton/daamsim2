function [alphas, alphas_ov] = calculate_alpha_batch(ground_speed_h, ground_int_speed, azimuth_vect)
    % Preallocate output with same size as input
    alphas = zeros(size(azimuth_vect));
    alphas_ov = zeros(size(azimuth_vect));

    for k = 1:numel(azimuth_vect)
        a = calculate_alpha(ground_speed_h, ground_int_speed, azimuth_vect(k));
        a_ov = calculate_alpha_ov(ground_speed_h, ground_int_speed, azimuth_vect(k));
        alphas(k) = a;
        alphas_ov(k) = a_ov;
    end
    alphas = reshape(alphas, size(azimuth_vect));
    alphas_ov = reshape(alphas_ov, size(azimuth_vect));
end
