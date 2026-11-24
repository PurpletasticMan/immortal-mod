package com.immortalmod.item;

import java.util.List;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.protocol.game.ClientboundSetEntityMotionPacket;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

/** Spear with long reach (set through attributes) whose right-click is a piercing lunge. */
public class LungeSpearItem extends Item {
	private final float damage;
	private final double speed;
	private final int cooldownTicks;

	public LungeSpearItem(Properties properties, float damage, double speed, int cooldownTicks) {
		super(properties);
		this.damage = damage;
		this.speed = speed;
		this.cooldownTicks = cooldownTicks;
	}

	@Override
	public InteractionResult use(Level level, Player player, InteractionHand hand) {
		ItemStack stack = player.getItemInHand(hand);
		if (level instanceof ServerLevel serverLevel) {
			Vec3 look = player.getLookAngle();
			AABB path = player.getBoundingBox().expandTowards(look.scale(7.0)).inflate(1.0);
			List<LivingEntity> targets = serverLevel.getEntitiesOfClass(LivingEntity.class, path, e -> e != player && e.isAlive() && !e.isAlliedTo(player));
			for (LivingEntity target : targets) {
				target.hurtServer(serverLevel, serverLevel.damageSources().playerAttack(player), damage);
			}
			player.setDeltaMovement(look.scale(speed));
			if (player instanceof ServerPlayer serverPlayer) {
				serverPlayer.connection.send(new ClientboundSetEntityMotionPacket(serverPlayer));
			}
			for (int i = 0; i < 12; i++) {
				Vec3 p = player.position().add(look.scale(i * 0.5)).add(0, 1.0, 0);
				serverLevel.sendParticles(ParticleTypes.CRIT, p.x, p.y, p.z, 3, 0.1, 0.1, 0.1, 0.05);
			}
			level.playSound(null, player.getX(), player.getY(), player.getZ(), SoundEvents.TRIDENT_RIPTIDE_3, SoundSource.PLAYERS, 1.0F, 1.0F);
			player.getCooldowns().addCooldown(stack, cooldownTicks);
		}
		return InteractionResult.SUCCESS;
	}
}
