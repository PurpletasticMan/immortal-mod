package com.immortalmod.item;

import java.util.List;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/** Sword whose right-click is a special attack: a shockwave that damages and blasts away everything around you. */
public class SlashSwordItem extends Item {
	private final double radius;
	private final float damage;
	private final int cooldownTicks;
	private final double knockback;

	public SlashSwordItem(Properties properties, double radius, float damage, int cooldownTicks, double knockback) {
		super(properties);
		this.radius = radius;
		this.damage = damage;
		this.cooldownTicks = cooldownTicks;
		this.knockback = knockback;
	}

	@Override
	public InteractionResult use(Level level, Player player, InteractionHand hand) {
		ItemStack stack = player.getItemInHand(hand);
		if (level instanceof ServerLevel serverLevel) {
			List<LivingEntity> targets = serverLevel.getEntitiesOfClass(
					LivingEntity.class,
					player.getBoundingBox().inflate(radius),
					e -> e != player && e.isAlive() && !e.isAlliedTo(player));
			for (LivingEntity target : targets) {
				target.hurtServer(serverLevel, serverLevel.damageSources().playerAttack(player), damage);
				Vec3 away = target.position().subtract(player.position()).multiply(1, 0, 1);
				if (away.lengthSqr() > 1.0E-4) {
					away = away.normalize().scale(knockback);
					target.push(away.x, 0.45, away.z);
				}
			}
			// ring of sweep particles around the player
			for (int i = 0; i < 24; i++) {
				double angle = i * (Math.PI * 2 / 24);
				serverLevel.sendParticles(ParticleTypes.SWEEP_ATTACK,
						player.getX() + Math.cos(angle) * radius * 0.6, player.getY() + 1.0, player.getZ() + Math.sin(angle) * radius * 0.6,
						1, 0, 0, 0, 0);
			}
			level.playSound(null, player.getX(), player.getY(), player.getZ(), SoundEvents.PLAYER_ATTACK_SWEEP, SoundSource.PLAYERS, 1.5F, 0.7F);
			level.playSound(null, player.getX(), player.getY(), player.getZ(), SoundEvents.LIGHTNING_BOLT_THUNDER, SoundSource.PLAYERS, 0.6F, 1.6F);
			player.getCooldowns().addCooldown(stack, cooldownTicks);
		}
		return InteractionResult.SUCCESS;
	}
}
