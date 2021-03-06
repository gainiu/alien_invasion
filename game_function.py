import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_event(event, ai_settings, screen, aliens, ship, bullets, stats):
    '''响应按键'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(ai_settings, screen, aliens, ship, bullets, stats)


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_event(event, ship):
    '''响应松开'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_event(ai_settings, screen, ship, bullets, aliens, play_button, stats, sb):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('alien_invasion/highscore.txt','w') as highscore_file:
                highscore_file.write(str(stats.high_score))
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_settings, screen,
                                aliens, ship, bullets, stats)

        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, ship, bullets,
                              aliens, play_button, stats, mouse_x, mouse_y, sb)


def check_play_button(ai_settings, screen, ship, bullets, aliens, play_button, stats, mouse_x, mouse_y, sb):
    '''在玩家单击Play按钮时开始新游戏'''
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        '''重置游戏统计信息'''
        start_game(ai_settings, screen, aliens, ship, bullets, stats, sb)


def start_game(ai_settings, screen, aliens, ship, bullets, stats, sb):
    ai_settings.initialize_dynamic_settings()
    # 隐藏光标
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    sb.prep_image()
    stats.game_active = True
    # 清空外星人列表和子弹列表
    bullets.empty()
    aliens.empty()
    # 创建一群新的外星人，并让飞船居中
    create_fleet(ai_settings, screen, aliens, ship)
    ship.center_ship()


def upgrade_screen(ai_settings, screen, ship, aliens, bullets, sb, stats, play_button):
    '''更新屏幕上的图像并切换到新屏幕'''
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 显示得分
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(bullets, aliens, ai_settings, screen, ship, stats, sb):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.top <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(
        ai_settings, screen, aliens, ship, bullets, stats, sb)


def check_high_score(stats, sb):
    '''检查是否诞生了新的最高分'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_alien_collisions(ai_settings, screen, aliens, ship, bullets, stats, sb):
    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points*len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, aliens, ship)
        stats.level+=1
        sb.prep_level()


def create_fleet(ai_settings, screen, aliens, ship):
    '''创建外星人群'''
    # 创建一个外星人，并计算一行可容纳多少个外星人
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_alien_x = get_number_aliens_x(ai_settings, screen, alien.rect.width)
    number_rows = get_number_rows(
        ai_settings, alien.rect.height, ship.rect.height)

    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings, screen, alien_number, aliens, row_number)


def get_number_aliens_x(ai_settings, screen, alien_width):
    '''计算一行可容纳多少个外星人'''
    available_space_x = ai_settings.screen_width - 2*alien_width
    number_alien_x = int(available_space_x/(2*alien_width))
    return number_alien_x


def create_alien(ai_settings, screen, alien_number, aliens, row_number):
    '''创建一个外星人并将其放置在当前行'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width+2*alien_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)


def get_number_rows(ai_settings, alien_height, ship_height):
    '''计算屏幕可容纳多少行外星人'''
    available_space_y = ai_settings.screen_height-3*alien_height-ship_height
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, aliens, ship, screen, stats, bullets, sb):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, aliens, ship, stats, bullets, sb)
    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, screen, aliens, ship, stats, bullets, sb)


def ship_hit(ai_settings, screen, aliens, ship, stats, bullets, sb):
    '''响应被外星人撞到的飞船'''
    if stats.ship_left > 0:
        # 将ship_left减1
        stats.ship_left -= 1
        sb.prep_ship()
        # 清空外星人列表和子弹列表
        bullets.empty()
        aliens.empty()
        # 创建一群新的外星人群组，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, aliens, ship, stats, bullets, sb):
    '''检查是否有外星人到达屏幕底端'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞一样进行处理
            ship_hit(ai_settings, screen, aliens, ship, stats, bullets, sb)
            break
