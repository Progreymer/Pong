# start_point = pygame.math.Vector2((ball.rect.x, ball.rect.y))
#                     end_point = pygame.math.Vector2((ball.rect.x + (HEIGHT - ball.rect.y)*ball.speed_x/float(c), HEIGHT))
#
#                     angle_in_radians = math.atan(float(c)/ball.speed_x)
#                     angle_in_degrees = math.degrees(angle_in_radians)
#                     print(angle_in_degrees)
#
#                     pygame.draw.line(screen, colors["White"], start_point, end_point, 1)
#
#                     start_point2 = pygame.math.Vector2(ball.rect.x + (HEIGHT - ball.rect.y)*ball.speed_x/float(c), HEIGHT)
#                     end_point2 = pygame.math.Vector2( (-(HEIGHT - ball.rect.y)*ball.speed_x/float(c))*ball.speed_x/ball.speed_y,0 )
#
#                     if not meet_point_set:
#                         ai_meet_point = end_point2
#                         meet_point_set = True
#
#                     start_point2.rotate(-angle_in_degrees)
#
#                     current_endpoint = start_point + end_point.rotate(-angle_in_degrees)
#
#                     pygame.draw.line(screen, colors["Red"],start_point2, ai_meet_point, 1)
#
#                 #(ball.rect.x + (HEIGHT - ball.rect.y)*ball.speed_x/float(c), HEIGHT),(0, (ball.speed_y - (HEIGHT - ball.rect.y)*ball.speed_x/float(c))* -(ball.speed_y/ball.speed_x ))
#                 if ball.speed_y < 0:
#                     start_point = pygame.math.Vector2(ball.rect.centerx, ball.rect.centery)
#                     end_point = pygame.math.Vector2((ball.rect.x - (0 - ball.rect.y) * ball.speed_x / float(c), 0))
#
#                     angle_in_radians = math.atan(float(c) / ball.speed_x)
#                     angle_in_degrees = math.degrees(angle_in_radians)
#                     print(angle_in_degrees)
#
#                     pygame.draw.line(screen, colors["White"], start_point, end_point, 1)
#
#                     start_point2 = pygame.math.Vector2(ball.rect.x - (0 - ball.rect.y) * ball.speed_x / float(c), 0)
#                     end_point2 = pygame.math.Vector2((ball.rect.x - (0 - ball.rect.y) * ball.speed_x / float(c)) * ball.speed_x / ball.speed_y, 0)
#
#                     start_point2.rotate(-angle_in_degrees)
