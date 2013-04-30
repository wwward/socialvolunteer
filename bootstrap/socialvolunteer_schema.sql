SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `groupwerk` DEFAULT CHARACTER SET latin1 ;
USE `groupwerk` ;

-- -----------------------------------------------------
-- Table `groupwerk`.`Friends`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Friends` (
  `id` VARCHAR(30) NULL DEFAULT NULL ,
  `friend_id` VARCHAR(30) NULL DEFAULT NULL )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

CREATE INDEX `Idx_friends` ON `groupwerk`.`Friends` (`id` ASC) ;


-- -----------------------------------------------------
-- Table `groupwerk`.`Job`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Job` (
  `id` VARCHAR(30) NULL DEFAULT NULL ,
  `organization_id` VARCHAR(30) NULL DEFAULT NULL ,
  `event_date` DATE NULL DEFAULT NULL ,
  `event_time` TIME NULL DEFAULT NULL ,
  `event_duration_minutes` SMALLINT(6) NULL DEFAULT NULL ,
  `score_value` SMALLINT(6) NULL DEFAULT NULL ,
  `description` VARCHAR(255) NULL DEFAULT NULL ,
  `category` VARCHAR(255) NULL DEFAULT NULL ,
  `status` SMALLINT(6) NULL DEFAULT NULL )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `groupwerk`.`Job_volunteer`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Job_volunteer` (
  `job_id` VARCHAR(30) NULL DEFAULT NULL ,
  `volunteer_id` VARCHAR(30) NULL DEFAULT NULL ,
  `committed` SMALLINT(6) NULL DEFAULT NULL ,
  `completed` SMALLINT(6) NULL DEFAULT NULL ,
  `checkedin` SMALLINT(6) NULL DEFAULT NULL ,
  `checkedout` SMALLINT(6) NULL DEFAULT NULL )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `groupwerk`.`Keyword`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Keyword` (
  `keyword` VARCHAR(30) NULL DEFAULT NULL ,
  `reference_id` VARCHAR(30) NULL DEFAULT NULL )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

CREATE INDEX `Idx_keyword` ON `groupwerk`.`Keyword` (`keyword` ASC) ;


-- -----------------------------------------------------
-- Table `groupwerk`.`Organization`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Organization` (
  `id` VARCHAR(30) NULL DEFAULT NULL ,
  `name` VARCHAR(60) NULL DEFAULT NULL ,
  `phone` VARCHAR(15) NULL DEFAULT NULL ,
  `location` VARCHAR(60) NULL DEFAULT NULL ,
  `reputation` SMALLINT(6) NULL DEFAULT NULL ,
  `description` VARCHAR(100) NULL DEFAULT NULL )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

CREATE INDEX `Idx_organization` ON `groupwerk`.`Organization` (`location` ASC) ;


-- -----------------------------------------------------
-- Table `groupwerk`.`Score`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Score` (
  `id` VARCHAR(30) NULL DEFAULT NULL ,
  `job_id` VARCHAR(30) NULL DEFAULT NULL ,
  `score` SMALLINT(6) NULL DEFAULT NULL )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

CREATE INDEX `Idx_score` ON `groupwerk`.`Score` (`id` ASC) ;


-- -----------------------------------------------------
-- Table `groupwerk`.`Volunteer`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `groupwerk`.`Volunteer` (
  `id` VARCHAR(30) NULL DEFAULT NULL ,
  `name` VARCHAR(60) NULL DEFAULT NULL ,
  `phone` VARCHAR(15) NULL DEFAULT NULL ,
  `location` VARCHAR(60) NULL DEFAULT NULL ,
  `friends` VARCHAR(30) NULL DEFAULT NULL ,
  `total_score` SMALLINT(6) NULL DEFAULT NULL ,
  `reputation` SMALLINT(6) NULL DEFAULT NULL ,
  `username` VARCHAR(30) NULL DEFAULT NULL )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

CREATE INDEX `Idx_volunteer` ON `groupwerk`.`Volunteer` (`location` ASC) ;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
